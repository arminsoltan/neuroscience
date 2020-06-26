from phases import phase3, phase4

if __name__ == '__main__':
    phase_number = input("which phase do you want to execute?: ").strip()
    task_number = input("which task do you want to execute?: ")
    FUNC = {
        "3": {
            '1': phase3.task_1,
            '2': phase3.task_2,
            '3': phase3.task_3
        },
        "4": {
            '1': phase4.task_1,
            '2': phase4.task_2
        }
    }
    FUNC[phase_number][task_number]()

