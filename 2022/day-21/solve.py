from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.jobs = dict()
        for line in text.splitlines():
            parts = line.split(": ")
            name = parts[0]
            if parts[1].isnumeric():
                data.jobs[name] = int(parts[1])
            else:
                data.jobs[name] = parts[1].split(" ")

    def compute(self, data):
        return self.do_job(data.jobs, "root")

    def do_job(self, jobs, name):
        job = jobs[name]
        if type(job) == int:
            return job

        operand1 = self.do_job(jobs, job[0])
        operand2 = self.do_job(jobs, job[2])
        match job[1]:
            case "+":
                return operand1 + operand2
            case "-":
                return operand1 - operand2
            case "*":
                return operand1 * operand2
            case "/":
                return operand1 // operand2

    def example_answer(self):
        return 152


class PartB(PartA):
    def compute(self, data):
        data.humn_jobs = dict()
        self.do_humn_jobs(data, "humn")
        return data.result

    def do_humn_jobs(self, data, name):
        key, job = self.find_job_with(data, name)
        if key == "root":
            to_solve = job[0] if job[0] != name else job[2]
            to_add = job[0] if job[0] == name else job[2]
            result = self.do_job(data.jobs, to_solve)
            data.humn_jobs[to_add] = result
            data.result = self.do_job(data.humn_jobs, "humn")
            return
        match job:
            case [arg1, "+", arg2]:
                other = arg1 if arg1 != name else arg2
                data.humn_jobs[name] = [key, "-", other]
                data.humn_jobs[other] = self.do_job(data.jobs, other)
                self.do_humn_jobs(data, key)
            case [arg1, "-", arg2]:
                if arg1 == name:
                    data.humn_jobs[name] = [key, "+", arg2]
                    data.humn_jobs[arg2] = self.do_job(data.jobs, arg2)
                    self.do_humn_jobs(data, key)
                else:
                    data.humn_jobs[name] = [arg1, "-", key]
                    data.humn_jobs[arg1] = self.do_job(data.jobs, arg1)
                    self.do_humn_jobs(data, key)
            case [arg1, "*", arg2]:
                other = arg1 if arg1 != name else arg2
                data.humn_jobs[name] = [key, "/", other]
                data.humn_jobs[other] = self.do_job(data.jobs, other)
                self.do_humn_jobs(data, key)
            case [arg1, "/", arg2]:
                if arg1 == name:
                    data.humn_jobs[name] = [arg2, "*", key]
                    data.humn_jobs[arg2] = self.do_job(data.jobs, arg2)
                    self.do_humn_jobs(data, key)
                else:
                    data.humn_jobs[name] = [arg1, "/", key]
                    data.humn_jobs[arg1] = self.do_job(data.jobs, arg1)
                    self.do_humn_jobs(data, key)

    def find_job_with(self, data, monkey):
        for key, job in data.jobs.items():
            if type(job) != int:
                if job[0] == monkey or job[2] == monkey:
                    return key, job

    def example_answer(self):
        return 301


Day.do_day(21, 2022, PartA, PartB)
