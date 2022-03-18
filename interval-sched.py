from dataclasses import dataclass


def main():
    all_intervals = [
        Interval(0, 20, "The President's Algorit"),
        Interval(2.5, 15, "Discre Mathematics"),
        Interval(8, 25, "Tajan of the Jungle"),
        Interval(19, 30, "Halting State"),
        Interval(23, 34, "Steiner's Tree"),
        Interval(32, 53, "The Four Volume Problem"),
        Interval(35, 51, "Programming Challenges"),
        Interval(46, 65, "Process Terminated"),
        Interval(52, 66, "Calculated Bets"),
    ]

    
    best_sched = get_best_sched(all_intervals)
    print("The schedule which minimizes the downtime is: \n\t- " + 
            "\n\t- ".join((str(s) for s in best_sched)))


@dataclass
class Interval:
    """A class to represent an interval"""
    start: float
    end: float
    name: str
    

def get_best_sched(intervals: list[Interval]):
    """Finds the schedule which minimizes downtime."""
    if len(intervals) == 0:
        return []

    max_start = min((i.end for i in intervals))
    starts = [i for i in intervals if i.start < max_start]
    new_intervals = [i for i in intervals if i.start >= max_start]

    if len(new_intervals) == 0:
        return [max(starts, key=lambda s: s.end - s.start)]

    return max([[s, *get_best_sched([i for i in new_intervals if i.start >= s.end])] for s in starts], 
    key=lambda sched: sum(inter.end - inter.start for inter in sched))

if __name__ == "__main__":
    main()
