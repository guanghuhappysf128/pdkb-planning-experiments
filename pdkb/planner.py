
import os, sys, time, pickle, json


from .actions import *
from .problems import *
from .translator import *

def cleanup():
    os.system('rm -f pdkb-domain.pddl')
    os.system('rm -f pdkb-problem.pddl')
    os.system('rm -f pdkb-plan.txt')
    os.system('rm -f pdkb-plan.out')
    os.system('rm -f pdkb-plan.out.err')
    os.system('rm -f execution.details')
    os.system('rm -f output.json')


def solve(pdkbddl_file, old_planner=False):

    print()

    t_start = time.time()
    problem = parse_and_preprocess(pdkbddl_file)
    precompliation_time = time.time() - t_start
    with open("output.json", "r") as f:
        output = json.load(f)
        output["precompilation_time"] = precompliation_time
    with open("output.json", "w") as f:
        json.dump(output, f)
    print("Solving problem...", end=' ')

    sys.stdout.flush()
    problem.solve(old_planner)
    print("done!")

    print("\nTime: %f s" % (time.time() - t_start))
    with open("output.json", "r") as f:
        output = json.load(f)
        output["total_time"] = time.time() - t_start
    with open("pdkb-plan.out", "r") as f:
        for line in f.readlines():
            if "Nodes generated during search:" in line:
                output["generated"] = int(line.split(":")[1])
            if "Nodes expanded during search:" in line:
                output["expanded"] = int(line.split(":")[1])
    with open("output.json", "w") as f:
        json.dump(output, f)
    problem.output_solution()

    print()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\nUsage: python planner.py <pdkbddl file> [--keep-files] [--old-planner]\n")
        sys.exit(1)

    solve(sys.argv[1], old_planner=('--old-planner' in sys.argv))

    if len(sys.argv) < 3 or '--keep-files' != sys.argv[2]:
        cleanup()
