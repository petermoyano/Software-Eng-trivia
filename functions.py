
ques_number = {1:'One', 2:'Two', 3:'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9:'Nine', 10:'Ten'}

def analize_answers(jsonr):
    """returns a list of lists, by Taking as an input a dictionary with available answers as values, 
    some of wich can be None and returns a list with the none None answers, to eventually iterate over
     to provide a dynamic id to the answer
    """
    iter_base = []
    for dict_quest in jsonr:
        answers = []
        for answer in dict_quest['answers'].values():
            if answer != None:
                answers.append(answer)
        iter_base.append(answers)
    return iter_base

test_jsonr = [{'id': 958, 'question': 'In Kubernetes, a node is:', 'description': None, 'answers': {'answer_a': 'A tool for starting a kubernetes cluster on a local machine', 'answer_b': 'A worker machine', 'answer_c': 'A machine that coordinates the scheduling and management of application containers on the cluster', 'answer_d': None, 'answer_e': None, 'answer_f': None}, 'multiple_inv_answers': 'false', 'inv_answers': {'answer_a_correct': 'false', 'answer_b_correct': 'true', 'answer_c_correct': 'false', 'answer_d_correct': 'false', 'answer_e_correct': 'false', 'answer_f_correct': 'false'}, 'correct_answer': None, 'explanation': None, 'tip': None, 'tags': [{'name': 'Kubernetes'}], 'category': 'DevOps', 'difficulty': 'Easy'}, {'id': 914, 'question': 'The Kubernetes Network proxy runs on which node?', 'description': None, 'answers': {'answer_a': 'Master Node', 'answer_b': 'Worker Node', 'answer_c': 'All the nodes', 'answer_d': 'None of the mentioned', 'answer_e': None, 'answer_f': None}, 'multiple_inv_answers': 'false', 'inv_answers': {'answer_a_correct': 'false', 'answer_b_correct': 'false', 'answer_c_correct': 'true', 'answer_d_correct': 'false', 'answer_e_correct': 'false', 'answer_f_correct': 'false'}, 'correct_answer': None, 'explanation': None, 'tip': None, 'tags': [{'name': 'Kubernetes'}], 'category': 'DevOps', 'difficulty': 'Easy'}, {'id': 1038, 'question': 'The default Ansible inventory file is located at:', 'description': None, 'answers': {'answer_a': '/home/ansible/inventory', 'answer_b': '/etc/ansible/inventory', 'answer_c': '/home/ansible/hosts', 'answer_d': '/etc/ansible/hosts', 'answer_e': None, 'answer_f': None}, 'multiple_inv_answers': 'false', 'inv_answers': {'answer_a_correct': 'false', 'answer_b_correct': 'false', 'answer_c_correct': 'false', 'answer_d_correct': 'true', 'answer_e_correct': 'false', 'answer_f_correct': 'false'}, 'correct_answer': 'answer_a', 'explanation': None, 'tip': None, 'tags': [{'name': 'DevOps'}], 'category': 'DevOps', 'difficulty': 'Easy'}, {'id': 960, 'question': 'What is a cluster?', 'description': None, 'answers': {'answer_a': 'A system made up of multiple servers and other resources', 'answer_b': 'A computer program or device that provides services to other computers', 'answer_c': 'A specific set of ordered operations', 'answer_d': 'A software package that performs a specific function for an end user', 'answer_e': None, 'answer_f': None}, 'multiple_inv_answers': 'false', 'inv_answers': {'answer_a_correct': 'true', 'answer_b_correct': 'false', 'answer_c_correct': 'false', 'answer_d_correct': 'false', 'answer_e_correct': 'false', 'answer_f_correct': 'false'}, 'correct_answer': None, 'explanation': None, 'tip': None, 'tags': [{'name': 'Kubernetes'}], 'category': 'DevOps', 'difficulty': 'Easy'}, {'id': 913, 'question': 'Which of the following are core Kubernetes objects?', 'description': None, 'answers': {'answer_a': 'Pods, Services, Volumes', 'answer_b': 'Pods, Docker, Volumes', 'answer_c': 'Pods, Services, Droplets', 'answer_d': 'None of the mentioned', 'answer_e': None, 'answer_f': None}, 'multiple_inv_answers': 'false', 'inv_answers': {'answer_a_correct': 'true', 'answer_b_correct': 'false', 'answer_c_correct': 'false', 'answer_d_correct': 'false', 'answer_e_correct': 'false', 'answer_f_correct': 'false'}, 'correct_answer': None, 'explanation': None, 'tip': None, 'tags': [{'name': 'Kubernetes'}], 'category': 'DevOps', 'difficulty': 'Easy'}]

def inverted_answers(jsonr):
    """Returns a list of dictionaries each one a reverse of the answers dict"""
    inv_answers = []
    for quest_dict in jsonr:
        inv_ans = {v:k for k, v in quest_dict['answers'].items()} 
        inv_answers.append(inv_ans)
    return inv_answers #[{bla: ans_a, bla: ans_b, blabla: ans_c}, {...:ans_a, ...:ans_b, ...}, {.,.,.}, ...]

def calculate_score(all_true_or_false):
    """Calculate the score based on the list all_true_or_false ["true", "true", "false", ...]"""
    count = 0
    for el in all_true_or_false:
        if el == "true":
            count += 1
    print(count, len(all_true_or_false))
    return count/len(all_true_or_false) * 100

def give_score(jsonr, all_responses): 
    """Verifies user responses and gives a score: The flow is as follows:
    all_responses = ["bla bla", "foo", "bar baz", ...] just a list of strings

    Step 1: reverse the answers dictionary by calling inverted_answers()
    Step 2: create a new list with the users answers in [answer_a, answer_c, ...] format.
    Step 3: convert the [answer_a, answer_c, ...] format in a ["true", "true", "false", ...] format and return that
    """
    #Step 1:
    inv_answers = inverted_answers(jsonr) #[{},{},{},...] see line 26
    #Step 2:
    all_responses_abc = [] #[answer_b, answer_a, answer_d, ...]
    for ans_as_string in all_responses:
        all_responses_abc.append(inv_answers[all_responses.index(ans_as_string)][ans_as_string])
    #Step 3: 
    all_true_or_false = [] #["true", "true", "false", ...]
    for quest_dict in jsonr:
        all_true_or_false.append(quest_dict["correct_answers"][f"{all_responses_abc[jsonr.index(quest_dict)]}_correct"])

    return calculate_score(all_true_or_false)

     



