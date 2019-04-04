# -*- coding: utf-8 -*-
# coding:utf-8
import random
import math
from wejudge.common.enums.judge import JudgeFlagsEnums
from wejudge.common.models.contest import Contest, ContestAccount, ContestJudgeStatus, ContestProblem
from faker import Faker


fake = Faker(locale='zh_CN')
contest = Contest.objects.get(id=1)

AVALIABLE_FLAG = [1, 2, 3, 4, 5, 6, 7]
RATIO_OF_AC = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
TIME_DURATION = contest.end_time - contest.start_time

accounts, problems = [], []
cps = ContestProblem.objects.filter(contest=contest)
for cp in cps:
    problems.append(cp)

for i in range(0, 100):
    p = fake.profile()
    ca = ContestAccount.objects.create(
        contest=contest,
        username=p.get('username'),
        role=0,
        is_enrolled=True,
        sex=1 if p.get('sex') == 'M' else 0,
        nickname=p.get('name'),
        realname=p.get('name'),
        schoolname=p.get('company'),
        coachname=fake.name()
    )
    ca.save()
    accounts.append(ca)
    print("创建账户 {0}；名字： {1}; username: {2}".format(i, ca.nickname, ca.username))

js_total = 2000 + random.randint(1, 1000)
TIME_INTERVAL = math.floor(TIME_DURATION / js_total)


def find_random_flag_ratio(author, problem):
    """
    根据概率来计算某用户对某题可能过题的情况
    :param author:
    :param problem:
    :return:
    """
    t = ContestJudgeStatus.objects.filter(
        author=author,
        problem=problem,
        flag=0
    )
    # 如果这个b没有过题
    if not t.exists():
        # 获取它提交次数
        subcnt = ContestJudgeStatus.objects.filter(
            author=author,
            problem=problem,
        ).count()
        if subcnt < len(RATIO_OF_AC):
            start_ratio = RATIO_OF_AC[subcnt]
        else:
            start_ratio = 100
        # 也就是说这个b提交了10次必定可以AC，看他运气了
        return random.randint(start_ratio, 100) >= 90
    else:
        return None


for i in range(0, js_total):
    a = accounts[random.randint(0, len(accounts) - 1)]
    cp = problems[random.randint(0, len(problems) - 1)]
    f = find_random_flag_ratio(a, cp.problem)
    print("创建虚拟评测 {0} (题目{1})...".format(i, cp.order), end='')
    if f is None:
        # 如果这个b已经过题了，给别人一些机会8
        print()
        continue
    flag = 0 if f else AVALIABLE_FLAG[random.randint(0, len(AVALIABLE_FLAG) - 1)]
    cjs = ContestJudgeStatus.objects.create(
        problem=cp.problem,
        contest_problem_item=cp,
        contest=contest,
        author=a,
        flag=flag,
        code_lang=1,
    )
    cjs.save()
    cjs.create_time = contest.start_time + random.randint(TIME_INTERVAL * i, TIME_INTERVAL * (i+1))
    cjs.save()
    print("{}".format(JudgeFlagsEnums.from_value(cjs.flag).get_desc().get('title', '未知')))
