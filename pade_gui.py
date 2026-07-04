from pade_constants import (
    Colors,
    ArmorLabelSettings,
    PenLabelSettings,
    AngleLabelSettings,
    EffPenLabelSettings,
    KillLabelSettings,
    ShadowSettings,
)
from gambiter import g_guiFlash  # type: ignore
from gambiter.flash import COMPONENT_TYPE, COMPONENT_ALIGN  # type: ignore


def log(message):
    print("pademinune's Gui: " + str(message))


ARMOR_ALIAS = "pademinune_ArmorLabel"
PEN_ALIAS = "pademinune_PenLabel"
ANGLE_ALIAS = "pademinune_AngleLabel"
EFF_PEN_ALIAS = "pademinune_EffPenLabel"
KILL_ALIAS = "pademinune_KillLabel"


class GuiState(object):
    def __init__(self):
        self.armor_label = Label(ARMOR_ALIAS, ArmorLabelSettings)
        self.pen_label = Label(PEN_ALIAS, PenLabelSettings)
        self.angle_label = AngleLabel(ANGLE_ALIAS, AngleLabelSettings)
        self.eff_pen_label = Label(EFF_PEN_ALIAS, EffPenLabelSettings)
        self.kill_label = Label(KILL_ALIAS, KillLabelSettings)
        self.labels = [
            self.armor_label,
            self.pen_label,
            self.angle_label,
            self.eff_pen_label,
            self.kill_label,
        ]

    def is_visible(self):
        for label in self.labels:
            if label.visible:
                return True
        return False

    def hide_all(self):
        for label in self.labels:
            if label.visible:
                label.hide()

    def update_gui(
        self,
        armor_value,
        prob,
        ricochet,
        hit_body,
        hit_track,
        hit_angle,
        avg_pen,
        kill_prob,
    ):
        if ricochet:
            # shell ricochet
            color = Colors.PURPLE
            if self.armor_label.settings.ENABLED:
                self.armor_label.update_gui("-", color)
            if self.pen_label.settings.ENABLED:
                self.pen_label.update_gui(0, color)
            if self.angle_label.settings.ENABLED:
                self.angle_label.update_gui(hit_angle, color)
            if self.eff_pen_label.settings.ENABLED:
                self.eff_pen_label.update_gui(int(avg_pen), color)
            if self.kill_label.settings.ENABLED and self.kill_label.visible:
                self.kill_label.hide()
        elif not hit_body:
            # shell only hits spaced armor or tracks
            self.hide_all()
        else:
            color = Colors.get_color_from_prob(prob)

            if self.armor_label.settings.ENABLED:
                self.armor_label.update_gui(int(armor_value), color)
            if self.pen_label.settings.ENABLED:
                self.pen_label.update_gui(int(prob), color)
            if self.angle_label.settings.ENABLED:
                self.angle_label.update_gui(hit_angle, color)
            if self.eff_pen_label.settings.ENABLED:
                self.eff_pen_label.update_gui(int(avg_pen), color)
            if self.kill_label.settings.ENABLED:
                if kill_prob > 0:
                    self.kill_label.update_gui(
                        kill_prob, Colors.get_color_from_prob(kill_prob)
                    )
                elif self.kill_label.visible:
                    self.kill_label.hide()

    def update_properties(self):
        for label in self.labels:
            label.update_properties()


class Label(object):
    def __init__(self, alias, settings):
        self.alias = alias
        self.settings = settings
        self.visible = False
        self.last_text = None
        properties = {
            "isHtml": True,
            "text": "",
            "glowfilter": _build_glowfilter(),
            "alignX": COMPONENT_ALIGN.CENTER,
            "alignY": COMPONENT_ALIGN.CENTER,
            "x": settings.X_OFFSET,
            "y": settings.Y_OFFSET,
            "visible": False,
        }
        g_guiFlash.createComponent(alias, COMPONENT_TYPE.LABEL, properties)

    def hide(self):
        if self.visible:
            g_guiFlash.updateComponent(self.alias, {"visible": False})
            self.visible = False
            self.last_text = None

    def update_gui(self, value, color):
        interior_text = self.settings.LABEL_FORMAT.format(value=value)
        new_text = "<font size='{font_size}' color='#{color}' face='$FieldFont'>{interior_text}</font>".format(
            font_size=self.settings.FONT_SIZE, color=color, interior_text=interior_text
        )

        if new_text == self.last_text and self.visible:
            return

        self.last_text = new_text
        self.visible = True
        g_guiFlash.updateComponent(self.alias, {"text": new_text, "visible": True})

    def update_properties(self):
        new_properties = {
            "x": self.settings.X_OFFSET,
            "y": self.settings.Y_OFFSET,
            "glowfilter": _build_glowfilter(),
        }
        if not self.settings.ENABLED:
            self.hide()
        g_guiFlash.updateComponent(self.alias, new_properties)


class AngleLabel(Label):
    def __init__(self, alias, settings):
        super(AngleLabel, self).__init__(alias, settings)

    def update_gui(self, value, color):
        if value < self.settings.DISPLAY_THRESHOLD:
            self.hide()
            return
        super(AngleLabel, self).update_gui(value, color)


def _build_glowfilter():
    return {
        "color": int(ShadowSettings.COLOR, 16),
        "alpha": ShadowSettings.ALPHA / 10.0,
        "blurX": ShadowSettings.LENGTH,
        "blurY": ShadowSettings.LENGTH,
        "strength": ShadowSettings.STRENGTH,
        "quality": 2,
    }


log("Starting creation of armor and penetration gui components")


gui_state = GuiState()


log("GUI components have been created!")
