# -*- coding: utf-8 -*-
"""Diagnostic compatibility layer for Armor Penetration Calculator.

The filename intentionally starts with ``mod_zz_`` so the WoT mod loader imports
it after ``mod_armor_pen_calculator``. Diagnostics are throttled: every unique
warning or traceback is printed only once per game session.
"""

import traceback

from AvatarInputHandler import AvatarInputHandler, gun_marker_ctrl  # type: ignore
from PlayerEvents import g_playerEvents  # type: ignore


_PREFIX = "[ArmorCalc][DIAG]"
_seen = set()


def _log(message):
    print("%s %s" % (_PREFIX, message))


def _log_once(key, message):
    if key in _seen:
        return
    _seen.add(key)
    _log(message)


def _safe_type_name(value):
    try:
        return value.__class__.__name__
    except Exception:
        return "<unknown>"


def _interesting_attrs(value):
    """Return likely replacement API fields without dumping huge objects."""
    if value is None:
        return []

    result = []
    try:
        for name in dir(value):
            lowered = name.lower()
            if (
                "jet" in lowered
                or "loss" in lowered
                or "pierc" in lowered
                or "dist" in lowered
                or "armor" in lowered
                or "damage" in lowered
                or "shield" in lowered
            ):
                result.append(name)
    except Exception as error:
        return ["<dir failed: %s>" % error]

    return sorted(result)[:80]


def _log_exception(context, error):
    try:
        trace = traceback.format_exc()
    except Exception:
        trace = "traceback unavailable"

    signature = "%s:%s:%s" % (context, _safe_type_name(error), str(error))
    _log_once(
        "exception:" + signature,
        "%s failed: %s: %s\n%s" % (
            context,
            _safe_type_name(error),
            error,
            trace,
        ),
    )


def _inspect_api(cls):
    required = (
        "_SHELL_EXTRA_DATA",
        "_CRIT_ONLY_SHOT_RESULT",
        "_shouldRicochet",
        "_computePenetrationArmor",
        "_CrosshairShotResults__isDestructibleComponent",
        "_CrosshairShotResults__collectDebugPiercingData",
        "_CrosshairShotResults__sendDebugInfo",
    )

    missing = [name for name in required if not hasattr(cls, name)]
    if missing:
        _log_once(
            "missing-crosshair-api",
            "CrosshairShotResults API changed. Missing: %s. Candidates: %s"
            % (", ".join(missing), ", ".join(_interesting_attrs(cls))),
        )
    else:
        _log_once("crosshair-api-ok", "Required CrosshairShotResults API is present.")


def _inspect_shell(cls, shell):
    kind = getattr(shell, "kind", "<missing>")
    key = "shell-kind:%s" % kind
    if key in _seen:
        return
    _seen.add(key)

    _log("Shell kind=%s, type=%s, shell attrs=%s" % (
        kind,
        _safe_type_name(shell),
        ", ".join(_interesting_attrs(shell)),
    ))

    extra_map = getattr(cls, "_SHELL_EXTRA_DATA", None)
    if extra_map is None:
        _log_once(
            "missing-shell-extra-map",
            "_SHELL_EXTRA_DATA is absent. Crosshair class candidates: %s"
            % ", ".join(_interesting_attrs(cls)),
        )
        return

    try:
        extra = extra_map[kind]
    except Exception as error:
        _log_exception("_SHELL_EXTRA_DATA[%s]" % kind, error)
        return

    attrs = _interesting_attrs(extra)
    if hasattr(extra, "jetLossPPByDist"):
        try:
            value = getattr(extra, "jetLossPPByDist")
        except Exception as error:
            value = "<read failed: %s>" % error
        _log("shellExtraData kind=%s has jetLossPPByDist=%s; candidates=%s" % (
            kind,
            value,
            ", ".join(attrs),
        ))
    else:
        _log_once(
            "missing-jetLossPPByDist:%s" % kind,
            "shellExtraData kind=%s no longer has jetLossPPByDist. Using 0.0. "
            "Possible replacement fields: %s" % (kind, ", ".join(attrs)),
        )


def _inspect_collision(collisions_details):
    try:
        if not collisions_details:
            _log_once("empty-collisions", "Collision list is empty.")
            return
        first = collisions_details[0]
    except Exception as error:
        _log_exception("collision inspection", error)
        return

    _log_once(
        "collision-shape",
        "Collision object type=%s; relevant attrs=%s"
        % (_safe_type_name(first), ", ".join(_interesting_attrs(first))),
    )

    mat_info = getattr(first, "matInfo", None)
    if mat_info is not None:
        _log_once(
            "material-shape",
            "Material object type=%s; relevant attrs=%s"
            % (_safe_type_name(mat_info), ", ".join(_interesting_attrs(mat_info))),
        )


def _install_crosshair_wrappers():
    cls = gun_marker_ctrl._CrosshairShotResults
    _inspect_api(cls)

    current_get = cls.getShotResult
    original_get = getattr(current_get, "__func__", current_get)

    def diagnostic_get_shot_result(
        wrapped_cls, gun_marker, excludeTeam=0, piercingMultiplier=1
    ):
        try:
            return original_get(
                wrapped_cls, gun_marker, excludeTeam, piercingMultiplier
            )
        except Exception as error:
            _log_exception("getShotResult", error)
            raise

    cls.getShotResult = classmethod(diagnostic_get_shot_result)

    default_name = "_CrosshairShotResults__shotResultDefault"
    if hasattr(cls, default_name):
        current_default = getattr(cls, default_name)
        original_default = getattr(current_default, "__func__", current_default)

        def diagnostic_default(
            wrapped_cls,
            gun_marker,
            collisions_details,
            full_piercing_power,
            shell,
            min_pp,
            max_pp,
            entity,
        ):
            _inspect_shell(wrapped_cls, shell)
            _inspect_collision(collisions_details)
            try:
                return original_default(
                    wrapped_cls,
                    gun_marker,
                    collisions_details,
                    full_piercing_power,
                    shell,
                    min_pp,
                    max_pp,
                    entity,
                )
            except Exception as error:
                _log_once(
                    "default-context:%s" % getattr(shell, "kind", "unknown"),
                    "Default-shell failure context: shellKind=%s, fullPP=%s, "
                    "minPP=%s, maxPP=%s, entityType=%s"
                    % (
                        getattr(shell, "kind", "<missing>"),
                        full_piercing_power,
                        min_pp,
                        max_pp,
                        _safe_type_name(entity),
                    ),
                )
                _log_exception("__shotResultDefault", error)
                raise

        setattr(cls, default_name, classmethod(diagnostic_default))
    else:
        _log_once(
            "missing-default-method",
            "%s is absent. Available candidates: %s"
            % (default_name, ", ".join(_interesting_attrs(cls))),
        )

    modern_name = "_CrosshairShotResults__shotResultModernHE"
    if hasattr(cls, modern_name):
        current_modern = getattr(cls, modern_name)
        original_modern = getattr(current_modern, "__func__", current_modern)

        def diagnostic_modern_he(
            wrapped_cls,
            gun_marker,
            collisions_details,
            full_piercing_power,
            shell,
            min_pp,
            max_pp,
            entity,
        ):
            _inspect_shell(wrapped_cls, shell)
            _inspect_collision(collisions_details)
            try:
                return original_modern(
                    wrapped_cls,
                    gun_marker,
                    collisions_details,
                    full_piercing_power,
                    shell,
                    min_pp,
                    max_pp,
                    entity,
                )
            except Exception as error:
                _log_once(
                    "modern-context:%s" % getattr(shell, "kind", "unknown"),
                    "Modern-HE failure context: shellKind=%s, fullPP=%s, "
                    "minPP=%s, maxPP=%s, entityType=%s"
                    % (
                        getattr(shell, "kind", "<missing>"),
                        full_piercing_power,
                        min_pp,
                        max_pp,
                        _safe_type_name(entity),
                    ),
                )
                _log_exception("__shotResultModernHE", error)
                raise

        setattr(cls, modern_name, classmethod(diagnostic_modern_he))
    else:
        _log_once(
            "missing-modern-method",
            "%s is absent. Available candidates: %s"
            % (modern_name, ", ".join(_interesting_attrs(cls))),
        )


def _install_gui_wrapper():
    try:
        import mod_armor_pen_calculator as calculator
    except Exception as error:
        _log_exception("import mod_armor_pen_calculator", error)
        return

    original_update = getattr(calculator, "call_update_gui", None)
    if original_update is None:
        _log_once(
            "missing-call-update-gui",
            "call_update_gui is absent from mod_armor_pen_calculator.",
        )
        return

    def diagnostic_update_gui(*args, **kwargs):
        try:
            return original_update(*args, **kwargs)
        except Exception as error:
            _log_once(
                "gui-context",
                "GUI update failed. args=%s kwargs=%s" % (args, kwargs),
            )
            _log_exception("call_update_gui", error)
            raise

    calculator.call_update_gui = diagnostic_update_gui


def _install_postmortem_wrapper():
    current = AvatarInputHandler.activatePostmortem

    def diagnostic_postmortem(self, *args, **kwargs):
        try:
            return current(self, *args, **kwargs)
        except Exception as error:
            _log_exception("AvatarInputHandler.activatePostmortem", error)
            raise

    AvatarInputHandler.activatePostmortem = diagnostic_postmortem


def _on_match_start():
    _log("Match started; diagnostic cache contains %d keys." % len(_seen))


def _on_match_end():
    _log("Match ended; diagnostic cache contains %d keys." % len(_seen))


try:
    _install_crosshair_wrappers()
    _install_gui_wrapper()
    _install_postmortem_wrapper()
    g_playerEvents.onAvatarBecomePlayer += _on_match_start
    g_playerEvents.onAvatarBecomeNonPlayer += _on_match_end
    _log("Diagnostic wrappers installed successfully.")
except Exception as error:
    _log_exception("diagnostic module initialization", error)
