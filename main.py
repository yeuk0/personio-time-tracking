from ptt.inputter import Inputter
from ptt.navigator import Navigator


if __name__ == "__main__":
    navigator = Navigator('firefox')

    navigator.load()

    navigator.go_to_attendance_page()

    inputter = Inputter('09:00', '17:00')
    for day, button in navigator.get_day_buttons().items():
        navigator.open_input_dialog(button)

        time_track = inputter.calculate_input_hours(day)
        navigator.log_time(time_track)

        navigator.close_input_dialog()

    navigator.quit()
