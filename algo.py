
import numpy as numpy

house_count = 1000

def compute_score(l, distance = 0, last_pos = 0):
    score = 0
    for e in l:
        distance += numpy.abs(e - last_pos)
        score += distance
        last_pos = e
    return score

def greedy(tmp: list):
    l = tmp.copy()
    result = []
    last_pos = 0
    while len(l) > 0:
        min_distance = 9999999999
        min_idx = 0
        for j in range(0, len(l)):
            if numpy.abs(l[j] - last_pos) < min_distance:
                min_distance = numpy.abs(l[j] - last_pos)
                min_idx = j
        result.append(l[min_idx])
        last_pos = l[min_idx]
        del l[min_idx]
    return result

def not_close(a, b):
    return numpy.abs(a - b) > 0.0001

def rec_case(todo: list, result: list, cur_pos, idx, dist, score, best_score, last_is_left) -> (float, list):
    if score >= best_score:
        return (score, result)
    if len(todo) == 1:
        score += compute_score(todo, distance=dist, last_pos=cur_pos)
        result.append(todo[0])
        return (score, result)
    if todo[idx] > cur_pos:
        score += compute_score(todo, distance=dist, last_pos=cur_pos)
        result.extend(todo)
        return (score, result)
    if idx + 1 >= len(todo):
        todo.reverse()
        score += compute_score(todo, distance=dist, last_pos=cur_pos)
        result.extend(todo)
        return (score, result)
    closest_is_left = numpy.abs(cur_pos - todo[idx]) < numpy.abs(cur_pos - todo[idx + 1])
    left = None
    if last_is_left != 0 or closest_is_left:
        tmp_todo_left = todo.copy()
        result_left = result.copy()
        tmp_pos = todo[idx]
        tmp_distance = dist + numpy.abs(tmp_pos - cur_pos)
        result_left.append(todo[idx])
        del tmp_todo_left[idx]
        left = rec_case(tmp_todo_left, result_left, tmp_pos, idx - 1, tmp_distance, score + tmp_distance, best_score, 1)
    right = None
    if last_is_left != 1 or not closest_is_left:
        tmp_todo = todo.copy()
        result_right = result.copy()
        tmp_pos = todo[idx + 1]
        tmp_distance = dist + numpy.abs(tmp_pos - cur_pos)
        result_right.append(todo[idx + 1])
        del tmp_todo[idx + 1]
        right = rec_case(tmp_todo, result_right, tmp_pos, idx, tmp_distance, score + tmp_distance, best_score, 0)
    if right == None:
        return left
    if left == None:
        return right
    if left[0] > right[0]:
        return right
    return left


def stupid_algo(l : list):
    score = compute_score(l.copy())
    result = l.copy()
    sorted_list = sorted(l.copy())
    tmp_score = compute_score(sorted_list)
    if tmp_score < score:
        score = tmp_score
        result = sorted_list
    sorted_list.reverse()
    tmp_score = compute_score(sorted_list)
    if tmp_score < score:
        score = tmp_score
        result = sorted_list
    greedy_list = greedy(l.copy())
    tmp_score = compute_score(greedy_list)
    if tmp_score < score:
        score = tmp_score
        result = greedy_list
    return result

def test_algo(l: list):
    sorted_list = sorted(l)
    start_idx = 0
    while start_idx < len(l):
        if sorted_list[start_idx] > 0:
            break
        start_idx = start_idx + 1
    if start_idx == 0:
        return sorted_list
    if start_idx == len(sorted_list):
        sorted_list.reverse()
        return sorted_list
    tmp_score = compute_score(stupid_algo(l))
    return rec_case(sorted_list, [], 0, start_idx - 1, 0, 0, tmp_score, -1)[1]    

# avg_percent=0
# count=0
# while 1:
#     l =  numpy.random.normal(0,1000,house_count).tolist()
#     greedy_list = greedy(l.copy())
#     stupid_list = stupid_algo(l.copy())
#     greedy_score = compute_score(greedy_list)
#     stupid_score = compute_score(stupid_list)
#     tmp_percent = (greedy_score - stupid_score) * 100 / stupid_score
#     avg_percent = (avg_percent * count + tmp_percent) / count + 1
#     count = count + 1
#     print("avg = " + str(avg_percent) + "%")

avg_percent = 0
count = 0
while 1:
    l =  numpy.random.normal(0,10,house_count).tolist()
    algo_score = compute_score(greedy(l.copy()))
    greedy_score = compute_score(test_algo(l))
    reference_score = compute_score(l)
    sorted_list = sorted(l.copy())
    sort_score = compute_score(sorted_list)
    sorted_list.reverse()
    rev_sort_score = compute_score(sorted_list)
    greedy_percent = (reference_score - greedy_score) * 100 / reference_score
    algo_percent = (reference_score - algo_score) * 100 / reference_score
    sort_percent = (reference_score - sort_score) * 100 / reference_score
    rev_sort_percent = (reference_score - rev_sort_score) * 100 / reference_score

    print("greedy\t" + str(greedy_percent))
    print("my algo\t" + str(algo_percent))
    print("sort\t" + str(sort_percent))
    print("rev sort\t" + str(rev_sort_percent))

    # tmp_percent = (greedy_score - algo_score) * 100 / algo_score
    # avg_percent = ((avg_percent * count) + tmp_percent) / (count + 1)
    # count = count + 1
    # print("avg = " + str(avg_percent) + "\ttmp = " + str(tmp_percent))
    # if greedy_score < algo_score:
    #     print(l)

