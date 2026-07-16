# -*- coding: utf-8 -*-
from gui.modsSettingsApi import g_modsSettingsApi, templates  # type: ignore

try:
    from helpers import getClientLanguage  # type: ignore
except ImportError:
    getClientLanguage = None

from pade_constants import (
    ArmorLabelSettings,
    PenLabelSettings,
    AngleLabelSettings,
    EffPenLabelSettings,
    KillLabelSettings,
    Colors,
    ShadowSettings,
)
from pade_config import save_flat_config
from pade_gui import gui_state


mod_linkage = "pade_armor_calculator"
modDataVersion = 2


TRANSLATIONS = {
    "en": {
        "mod_name": "pademinune's Armor Penetration Calculator",
        "armor_section": "Armor Label",
        "armor_enable": "Enable Armor Label",
        "armor_enable_tip": "Show or hide the penetration/armor label.",
        "armor_size": "Armor Label Font Size",
        "armor_size_tip": "Font size of the penetration/armor label in pixels.",
        "armor_x": "Armor Label Horizontal Offset",
        "armor_x_tip": "Horizontal offset from screen center. Positive values move it right.",
        "armor_y": "Armor Label Vertical Offset",
        "armor_y_tip": "Vertical offset from screen center. Positive values move it down.",
        "armor_format": "Armor Label Format",
        "armor_format_tip": "Format of the label. {penetration} is current penetration, {armor} is effective armor.",
        "prob_section": "Probability Label",
        "prob_enable": "Enable Probability Label",
        "prob_enable_tip": "Show or hide the penetration probability label.",
        "prob_size": "Probability Label Font Size",
        "prob_size_tip": "Font size of the probability label in pixels.",
        "prob_x": "Probability Label Horizontal Offset",
        "prob_x_tip": "Horizontal offset from screen center. Positive values move it right.",
        "prob_y": "Probability Label Vertical Offset",
        "prob_y_tip": "Vertical offset from screen center. Positive values move it down.",
        "prob_format": "Probability Label Format",
        "prob_format_tip": "Format of the probability label. {value} is the penetration chance.",
        "angle_section": "Angle Label",
        "angle_enable": "Enable Angle Label",
        "angle_enable_tip": "Show or hide the impact angle label.",
        "angle_size": "Angle Label Font Size",
        "angle_size_tip": "Font size of the angle label in pixels.",
        "angle_x": "Angle Label Horizontal Offset",
        "angle_x_tip": "Horizontal offset from screen center. Positive values move it right.",
        "angle_y": "Angle Label Vertical Offset",
        "angle_y_tip": "Vertical offset from screen center. Positive values move it down.",
        "angle_format": "Angle Label Format",
        "angle_format_tip": "Format of the angle label. {value} is the impact angle in degrees.",
        "angle_threshold": "Angle Display Threshold",
        "angle_threshold_tip": "Minimum angle at which the label is shown. Set 0 to always show it.",
        "eff_section": "Effective Penetration Label",
        "eff_enable": "Enable Effective Penetration Label",
        "eff_enable_tip": "Show or hide the shell's current penetration label.",
        "eff_size": "Effective Penetration Font Size",
        "eff_size_tip": "Font size of the effective penetration label in pixels.",
        "eff_x": "Effective Penetration Horizontal Offset",
        "eff_x_tip": "Horizontal offset from screen center. Positive values move it right.",
        "eff_y": "Effective Penetration Vertical Offset",
        "eff_y_tip": "Vertical offset from screen center. Positive values move it down.",
        "eff_format": "Effective Penetration Format",
        "eff_format_tip": "Format of the penetration label. {value} is current penetration.",
        "kill_section": "Kill Chance Label",
        "kill_enable": "Enable Kill Chance Label",
        "kill_enable_tip": "Show or hide the estimated kill chance label.",
        "kill_size": "Kill Chance Font Size",
        "kill_size_tip": "Font size of the kill chance label in pixels.",
        "kill_x": "Kill Chance Horizontal Offset",
        "kill_x_tip": "Horizontal offset from screen center. Positive values move it right.",
        "kill_y": "Kill Chance Vertical Offset",
        "kill_y_tip": "Vertical offset from screen center. Positive values move it down.",
        "kill_format": "Kill Chance Format",
        "kill_format_tip": "Format of the kill chance label. {value} is the estimated chance.",
        "colors_section": "Colors",
        "color_high": "High Penetration Chance",
        "color_high_tip": "Color used when penetration chance is at least 93%.",
        "color_medium": "Medium Penetration Chance",
        "color_medium_tip": "Color used when penetration chance is between 8% and 92%.",
        "color_low": "Low Penetration Chance",
        "color_low_tip": "Color used when penetration chance is at most 7%.",
        "color_ricochet": "Ricochet",
        "color_ricochet_tip": "Color used when the shell will ricochet.",
        "shadow_section": "Shadow",
        "shadow_color": "Shadow Color",
        "shadow_color_tip": "Color of the text shadow or glow.",
        "shadow_alpha": "Shadow Opacity",
        "shadow_alpha_tip": "Shadow opacity: 0 is transparent, 10 is fully opaque.",
        "shadow_length": "Shadow Blur",
        "shadow_length_tip": "Blur radius of the text shadow.",
        "shadow_strength": "Shadow Strength",
        "shadow_strength_tip": "Strength of the text outline. Higher values make it sharper.",
    },
    "uk": {
        "mod_name": "Калькулятор пробиття броні pademinune",
        "armor_section": "Пробиття / броня",
        "armor_enable": "Показувати пробиття та броню",
        "armor_enable_tip": "Показує або приховує напис поточного пробиття та ефективної броні.",
        "armor_size": "Розмір шрифту пробиття / броні",
        "armor_size_tip": "Розмір шрифту напису пробиття та броні в пікселях.",
        "armor_x": "Горизонтальне зміщення пробиття / броні",
        "armor_x_tip": "Зміщення від центру екрана. Додатне значення пересуває напис праворуч.",
        "armor_y": "Вертикальне зміщення пробиття / броні",
        "armor_y_tip": "Зміщення від центру екрана. Додатне значення пересуває напис униз.",
        "armor_format": "Формат пробиття / броні",
        "armor_format_tip": "Формат напису: {penetration} — поточне пробиття, {armor} — ефективна броня.",
        "prob_section": "Імовірність пробиття",
        "prob_enable": "Показувати шанс пробиття",
        "prob_enable_tip": "Показує або приховує розрахункову ймовірність пробиття.",
        "prob_size": "Розмір шрифту шансу пробиття",
        "prob_size_tip": "Розмір шрифту ймовірності пробиття в пікселях.",
        "prob_x": "Горизонтальне зміщення шансу",
        "prob_x_tip": "Зміщення від центру екрана. Додатне значення пересуває напис праворуч.",
        "prob_y": "Вертикальне зміщення шансу",
        "prob_y_tip": "Зміщення від центру екрана. Додатне значення пересуває напис униз.",
        "prob_format": "Формат шансу пробиття",
        "prob_format_tip": "Формат напису. {value} замінюється шансом пробиття.",
        "angle_section": "Кут влучання",
        "angle_enable": "Показувати кут влучання",
        "angle_enable_tip": "Показує або приховує кут входження снаряда в броню.",
        "angle_size": "Розмір шрифту кута",
        "angle_size_tip": "Розмір шрифту кута в пікселях.",
        "angle_x": "Горизонтальне зміщення кута",
        "angle_x_tip": "Зміщення від центру екрана. Додатне значення пересуває напис праворуч.",
        "angle_y": "Вертикальне зміщення кута",
        "angle_y_tip": "Зміщення від центру екрана. Додатне значення пересуває напис униз.",
        "angle_format": "Формат кута",
        "angle_format_tip": "Формат напису. {value} замінюється кутом у градусах.",
        "angle_threshold": "Поріг показу кута",
        "angle_threshold_tip": "Мінімальний кут, з якого показується напис. Значення 0 показує його завжди.",
        "eff_section": "Окремий напис пробиття",
        "eff_enable": "Показувати окреме пробиття",
        "eff_enable_tip": "Показує або приховує окремий напис поточного пробиття снаряда.",
        "eff_size": "Розмір шрифту пробиття",
        "eff_size_tip": "Розмір шрифту окремого напису пробиття в пікселях.",
        "eff_x": "Горизонтальне зміщення пробиття",
        "eff_x_tip": "Зміщення від центру екрана. Додатне значення пересуває напис праворуч.",
        "eff_y": "Вертикальне зміщення пробиття",
        "eff_y_tip": "Зміщення від центру екрана. Додатне значення пересуває напис униз.",
        "eff_format": "Формат окремого пробиття",
        "eff_format_tip": "Формат напису. {value} замінюється поточним пробиттям.",
        "kill_section": "Шанс добивання",
        "kill_enable": "Показувати шанс добивання",
        "kill_enable_tip": "Показує або приховує розрахункову ймовірність пробити та знищити ціль.",
        "kill_size": "Розмір шрифту шансу добивання",
        "kill_size_tip": "Розмір шрифту шансу добивання в пікселях.",
        "kill_x": "Горизонтальне зміщення добивання",
        "kill_x_tip": "Зміщення від центру екрана. Додатне значення пересуває напис праворуч.",
        "kill_y": "Вертикальне зміщення добивання",
        "kill_y_tip": "Зміщення від центру екрана. Додатне значення пересуває напис униз.",
        "kill_format": "Формат шансу добивання",
        "kill_format_tip": "Формат напису. {value} замінюється шансом добивання.",
        "colors_section": "Кольори",
        "color_high": "Високий шанс пробиття",
        "color_high_tip": "Колір для шансу пробиття від 93%.",
        "color_medium": "Середній шанс пробиття",
        "color_medium_tip": "Колір для шансу пробиття від 8% до 92%.",
        "color_low": "Низький шанс пробиття",
        "color_low_tip": "Колір для шансу пробиття до 7%.",
        "color_ricochet": "Рикошет",
        "color_ricochet_tip": "Колір, коли снаряд має зрикошетити.",
        "shadow_section": "Тінь тексту",
        "shadow_color": "Колір тіні",
        "shadow_color_tip": "Колір тіні або світіння тексту.",
        "shadow_alpha": "Прозорість тіні",
        "shadow_alpha_tip": "Прозорість тіні: 0 — невидима, 10 — повністю непрозора.",
        "shadow_length": "Розмиття тіні",
        "shadow_length_tip": "Радіус розмиття тіні тексту.",
        "shadow_strength": "Сила тіні",
        "shadow_strength_tip": "Сила обведення тексту. Більше значення робить її чіткішою.",
    },
    "ru": {
        "mod_name": "Калькулятор пробития брони pademinune",
        "armor_section": "Пробитие / броня",
        "armor_enable": "Показывать пробитие и броню",
        "armor_enable_tip": "Показывает или скрывает текущее пробитие и эффективную броню.",
        "armor_size": "Размер шрифта пробития / брони",
        "armor_size_tip": "Размер шрифта пробития и брони в пикселях.",
        "armor_x": "Горизонтальное смещение пробития / брони",
        "armor_x_tip": "Смещение от центра экрана. Положительное значение перемещает надпись вправо.",
        "armor_y": "Вертикальное смещение пробития / брони",
        "armor_y_tip": "Смещение от центра экрана. Положительное значение перемещает надпись вниз.",
        "armor_format": "Формат пробития / брони",
        "armor_format_tip": "Формат надписи: {penetration} — текущее пробитие, {armor} — эффективная броня.",
        "prob_section": "Вероятность пробития",
        "prob_enable": "Показывать шанс пробития",
        "prob_enable_tip": "Показывает или скрывает расчётную вероятность пробития.",
        "prob_size": "Размер шрифта шанса пробития",
        "prob_size_tip": "Размер шрифта вероятности пробития в пикселях.",
        "prob_x": "Горизонтальное смещение шанса",
        "prob_x_tip": "Смещение от центра экрана. Положительное значение перемещает надпись вправо.",
        "prob_y": "Вертикальное смещение шанса",
        "prob_y_tip": "Смещение от центра экрана. Положительное значение перемещает надпись вниз.",
        "prob_format": "Формат шанса пробития",
        "prob_format_tip": "Формат надписи. {value} заменяется шансом пробития.",
        "angle_section": "Угол попадания",
        "angle_enable": "Показывать угол попадания",
        "angle_enable_tip": "Показывает или скрывает угол входа снаряда в броню.",
        "angle_size": "Размер шрифта угла",
        "angle_size_tip": "Размер шрифта угла в пикселях.",
        "angle_x": "Горизонтальное смещение угла",
        "angle_x_tip": "Смещение от центра экрана. Положительное значение перемещает надпись вправо.",
        "angle_y": "Вертикальное смещение угла",
        "angle_y_tip": "Смещение от центра экрана. Положительное значение перемещает надпись вниз.",
        "angle_format": "Формат угла",
        "angle_format_tip": "Формат надписи. {value} заменяется углом в градусах.",
        "angle_threshold": "Порог показа угла",
        "angle_threshold_tip": "Минимальный угол, с которого показывается надпись. Значение 0 показывает её всегда.",
        "eff_section": "Отдельная надпись пробития",
        "eff_enable": "Показывать отдельное пробитие",
        "eff_enable_tip": "Показывает или скрывает отдельную надпись текущего пробития снаряда.",
        "eff_size": "Размер шрифта пробития",
        "eff_size_tip": "Размер шрифта отдельной надписи пробития в пикселях.",
        "eff_x": "Горизонтальное смещение пробития",
        "eff_x_tip": "Смещение от центра экрана. Положительное значение перемещает надпись вправо.",
        "eff_y": "Вертикальное смещение пробития",
        "eff_y_tip": "Смещение от центра экрана. Положительное значение перемещает надпись вниз.",
        "eff_format": "Формат отдельного пробития",
        "eff_format_tip": "Формат надписи. {value} заменяется текущим пробитием.",
        "kill_section": "Шанс добивания",
        "kill_enable": "Показывать шанс добивания",
        "kill_enable_tip": "Показывает или скрывает вероятность пробить и уничтожить цель.",
        "kill_size": "Размер шрифта шанса добивания",
        "kill_size_tip": "Размер шрифта шанса добивания в пикселях.",
        "kill_x": "Горизонтальное смещение добивания",
        "kill_x_tip": "Смещение от центра экрана. Положительное значение перемещает надпись вправо.",
        "kill_y": "Вертикальное смещение добивания",
        "kill_y_tip": "Смещение от центра экрана. Положительное значение перемещает надпись вниз.",
        "kill_format": "Формат шанса добивания",
        "kill_format_tip": "Формат надписи. {value} заменяется шансом добивания.",
        "colors_section": "Цвета",
        "color_high": "Высокий шанс пробития",
        "color_high_tip": "Цвет для шанса пробития от 93%.",
        "color_medium": "Средний шанс пробития",
        "color_medium_tip": "Цвет для шанса пробития от 8% до 92%.",
        "color_low": "Низкий шанс пробития",
        "color_low_tip": "Цвет для шанса пробития до 7%.",
        "color_ricochet": "Рикошет",
        "color_ricochet_tip": "Цвет, когда снаряд должен срикошетить.",
        "shadow_section": "Тень текста",
        "shadow_color": "Цвет тени",
        "shadow_color_tip": "Цвет тени или свечения текста.",
        "shadow_alpha": "Прозрачность тени",
        "shadow_alpha_tip": "Прозрачность тени: 0 — невидимая, 10 — полностью непрозрачная.",
        "shadow_length": "Размытие тени",
        "shadow_length_tip": "Радиус размытия тени текста.",
        "shadow_strength": "Сила тени",
        "shadow_strength_tip": "Сила обводки текста. Большее значение делает её чётче.",
    },
}


def _get_language():
    language = "en"
    if getClientLanguage is not None:
        try:
            language = str(getClientLanguage()).lower().replace("-", "_")
        except Exception:
            language = "en"

    if language.startswith("uk") or language.startswith("ua"):
        return "uk"
    if language.startswith("ru"):
        return "ru"
    return "en"


TEXT = TRANSLATIONS[_get_language()]


def tr(key):
    return TEXT.get(key, TRANSLATIONS["en"].get(key, key))


def section(key):
    return templates.createLabel("<b>— %s —</b>" % tr(key))


def tip(header_key, body_key):
    return "{HEADER}%s{/HEADER}{BODY}%s{/BODY}" % (
        tr(header_key),
        tr(body_key),
    )


template = {
    "modDisplayName": tr("mod_name"),
    "enabled": True,
    "column1": [
        section("armor_section"),
        templates.createCheckbox(tr("armor_enable"), "armor_label_enabled", ArmorLabelSettings.ENABLED, tooltip=tip("armor_enable", "armor_enable_tip")),
        templates.createSlider(tr("armor_size"), "armor_label_font_size", ArmorLabelSettings.FONT_SIZE, 5, 100, 1, format="{{value}}px", tooltip=tip("armor_size", "armor_size_tip")),
        templates.createNumericStepper(tr("armor_x"), "armor_label_x_offset", ArmorLabelSettings.X_OFFSET, -2000, 2000, 1, manual=True, tooltip=tip("armor_x", "armor_x_tip")),
        templates.createNumericStepper(tr("armor_y"), "armor_label_y_offset", ArmorLabelSettings.Y_OFFSET, -2000, 2000, 1, manual=True, tooltip=tip("armor_y", "armor_y_tip")),
        templates.createInput(tr("armor_format"), "armor_label_format", ArmorLabelSettings.LABEL_FORMAT, tooltip=tip("armor_format", "armor_format_tip")),
        templates.createEmpty(10),
        section("prob_section"),
        templates.createCheckbox(tr("prob_enable"), "pen_label_enabled", PenLabelSettings.ENABLED, tooltip=tip("prob_enable", "prob_enable_tip")),
        templates.createSlider(tr("prob_size"), "pen_label_font_size", PenLabelSettings.FONT_SIZE, 5, 100, 1, format="{{value}}px", tooltip=tip("prob_size", "prob_size_tip")),
        templates.createNumericStepper(tr("prob_x"), "pen_label_x_offset", PenLabelSettings.X_OFFSET, -2000, 2000, 1, manual=True, tooltip=tip("prob_x", "prob_x_tip")),
        templates.createNumericStepper(tr("prob_y"), "pen_label_y_offset", PenLabelSettings.Y_OFFSET, -2000, 2000, 1, manual=True, tooltip=tip("prob_y", "prob_y_tip")),
        templates.createInput(tr("prob_format"), "pen_label_format", PenLabelSettings.LABEL_FORMAT, tooltip=tip("prob_format", "prob_format_tip")),
        templates.createEmpty(10),
        section("angle_section"),
        templates.createCheckbox(tr("angle_enable"), "angle_label_enabled", AngleLabelSettings.ENABLED, tooltip=tip("angle_enable", "angle_enable_tip")),
        templates.createSlider(tr("angle_size"), "angle_label_font_size", AngleLabelSettings.FONT_SIZE, 5, 100, 1, format="{{value}}px", tooltip=tip("angle_size", "angle_size_tip")),
        templates.createNumericStepper(tr("angle_x"), "angle_label_x_offset", AngleLabelSettings.X_OFFSET, -2000, 2000, 1, manual=True, tooltip=tip("angle_x", "angle_x_tip")),
        templates.createNumericStepper(tr("angle_y"), "angle_label_y_offset", AngleLabelSettings.Y_OFFSET, -2000, 2000, 1, manual=True, tooltip=tip("angle_y", "angle_y_tip")),
        templates.createInput(tr("angle_format"), "angle_label_format", AngleLabelSettings.LABEL_FORMAT, tooltip=tip("angle_format", "angle_format_tip")),
        templates.createNumericStepper(tr("angle_threshold"), "angle_label_display_threshold", AngleLabelSettings.DISPLAY_THRESHOLD, 0, 90, 1, manual=True, tooltip=tip("angle_threshold", "angle_threshold_tip")),
        templates.createEmpty(10),
        section("eff_section"),
        templates.createCheckbox(tr("eff_enable"), "eff_pen_label_enabled", EffPenLabelSettings.ENABLED, tooltip=tip("eff_enable", "eff_enable_tip")),
        templates.createSlider(tr("eff_size"), "eff_pen_label_font_size", EffPenLabelSettings.FONT_SIZE, 5, 100, 1, format="{{value}}px", tooltip=tip("eff_size", "eff_size_tip")),
        templates.createNumericStepper(tr("eff_x"), "eff_pen_label_x_offset", EffPenLabelSettings.X_OFFSET, -2000, 2000, 1, manual=True, tooltip=tip("eff_x", "eff_x_tip")),
        templates.createNumericStepper(tr("eff_y"), "eff_pen_label_y_offset", EffPenLabelSettings.Y_OFFSET, -2000, 2000, 1, manual=True, tooltip=tip("eff_y", "eff_y_tip")),
        templates.createInput(tr("eff_format"), "eff_pen_label_format", EffPenLabelSettings.LABEL_FORMAT, tooltip=tip("eff_format", "eff_format_tip")),
    ],
    "column2": [
        section("kill_section"),
        templates.createCheckbox(tr("kill_enable"), "kill_label_enabled", KillLabelSettings.ENABLED, tooltip=tip("kill_enable", "kill_enable_tip")),
        templates.createSlider(tr("kill_size"), "kill_label_font_size", KillLabelSettings.FONT_SIZE, 5, 100, 1, format="{{value}}px", tooltip=tip("kill_size", "kill_size_tip")),
        templates.createNumericStepper(tr("kill_x"), "kill_label_x_offset", KillLabelSettings.X_OFFSET, -2000, 2000, 1, manual=True, tooltip=tip("kill_x", "kill_x_tip")),
        templates.createNumericStepper(tr("kill_y"), "kill_label_y_offset", KillLabelSettings.Y_OFFSET, -2000, 2000, 1, manual=True, tooltip=tip("kill_y", "kill_y_tip")),
        templates.createInput(tr("kill_format"), "kill_label_format", KillLabelSettings.LABEL_FORMAT, tooltip=tip("kill_format", "kill_format_tip")),
        templates.createEmpty(10),
        section("colors_section"),
        templates.createColorChoice(tr("color_high"), "color_green", Colors.GREEN, tooltip=tip("color_high", "color_high_tip")),
        templates.createColorChoice(tr("color_medium"), "color_orange", Colors.ORANGE, tooltip=tip("color_medium", "color_medium_tip")),
        templates.createColorChoice(tr("color_low"), "color_red", Colors.RED, tooltip=tip("color_low", "color_low_tip")),
        templates.createColorChoice(tr("color_ricochet"), "color_ricochet", Colors.PURPLE, tooltip=tip("color_ricochet", "color_ricochet_tip")),
        templates.createEmpty(10),
        section("shadow_section"),
        templates.createColorChoice(tr("shadow_color"), "shadow_color", ShadowSettings.COLOR, tooltip=tip("shadow_color", "shadow_color_tip")),
        templates.createSlider(tr("shadow_alpha"), "shadow_alpha", ShadowSettings.ALPHA, 0, 10, 1, format="{{value}}", tooltip=tip("shadow_alpha", "shadow_alpha_tip")),
        templates.createSlider(tr("shadow_length"), "shadow_length", ShadowSettings.LENGTH, 0, 10, 1, format="{{value}}", tooltip=tip("shadow_length", "shadow_length_tip")),
        templates.createSlider(tr("shadow_strength"), "shadow_strength", ShadowSettings.STRENGTH, 0, 10, 1, format="{{value}}", tooltip=tip("shadow_strength", "shadow_strength_tip")),
    ],
}


def on_settings_save(linkage, new_settings):
    if linkage != mod_linkage:
        return

    ArmorLabelSettings.ENABLED = new_settings["armor_label_enabled"]
    ArmorLabelSettings.FONT_SIZE = new_settings["armor_label_font_size"]
    ArmorLabelSettings.X_OFFSET = new_settings["armor_label_x_offset"]
    ArmorLabelSettings.Y_OFFSET = new_settings["armor_label_y_offset"]
    ArmorLabelSettings.LABEL_FORMAT = new_settings["armor_label_format"]

    PenLabelSettings.ENABLED = new_settings["pen_label_enabled"]
    PenLabelSettings.FONT_SIZE = new_settings["pen_label_font_size"]
    PenLabelSettings.X_OFFSET = new_settings["pen_label_x_offset"]
    PenLabelSettings.Y_OFFSET = new_settings["pen_label_y_offset"]
    PenLabelSettings.LABEL_FORMAT = new_settings["pen_label_format"]

    AngleLabelSettings.ENABLED = new_settings["angle_label_enabled"]
    AngleLabelSettings.FONT_SIZE = new_settings["angle_label_font_size"]
    AngleLabelSettings.X_OFFSET = new_settings["angle_label_x_offset"]
    AngleLabelSettings.Y_OFFSET = new_settings["angle_label_y_offset"]
    AngleLabelSettings.LABEL_FORMAT = new_settings["angle_label_format"]
    AngleLabelSettings.DISPLAY_THRESHOLD = new_settings["angle_label_display_threshold"]

    EffPenLabelSettings.ENABLED = new_settings["eff_pen_label_enabled"]
    EffPenLabelSettings.FONT_SIZE = new_settings["eff_pen_label_font_size"]
    EffPenLabelSettings.X_OFFSET = new_settings["eff_pen_label_x_offset"]
    EffPenLabelSettings.Y_OFFSET = new_settings["eff_pen_label_y_offset"]
    EffPenLabelSettings.LABEL_FORMAT = new_settings["eff_pen_label_format"]

    KillLabelSettings.ENABLED = new_settings["kill_label_enabled"]
    KillLabelSettings.FONT_SIZE = new_settings["kill_label_font_size"]
    KillLabelSettings.X_OFFSET = new_settings["kill_label_x_offset"]
    KillLabelSettings.Y_OFFSET = new_settings["kill_label_y_offset"]
    KillLabelSettings.LABEL_FORMAT = new_settings["kill_label_format"]

    Colors.GREEN = new_settings["color_green"]
    Colors.ORANGE = new_settings["color_orange"]
    Colors.RED = new_settings["color_red"]
    Colors.PURPLE = new_settings["color_ricochet"]

    ShadowSettings.COLOR = new_settings["shadow_color"]
    ShadowSettings.ALPHA = new_settings["shadow_alpha"]
    ShadowSettings.LENGTH = new_settings["shadow_length"]
    ShadowSettings.STRENGTH = new_settings["shadow_strength"]

    save_flat_config(new_settings)
    gui_state.update_properties()


g_modsSettingsApi.setModTemplate(mod_linkage, template, on_settings_save, None)
