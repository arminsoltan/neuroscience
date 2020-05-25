from phases.phase3 import task_1, task_2, task_3

if __name__ == '__main__':
    number = input("which task do you want to execute?: ").strip()
    FUNC = {
        '1': task_1,
        '2': task_2,
        '3': task_3
    }
    FUNC[number]()
