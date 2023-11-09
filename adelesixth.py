#!/usr/bin/env python
# coding: utf-8

# In[147]:


import numpy as np


# In[148]:


# burst_array = np.array([1, 0.28, 0.45, 0.2, 0.75, 0.18, 0.22, 0.2, 0.45, 0.25, 0.22, 0.18, 0.8, 0.8, 0.16, 1, 0.1, 0.67, 1, 0, 1])
"""
skills_input is the main adjustable parameter in this script. To adjust for your purpose, for each skill, do the following:
- adjust ba_percent to be the percent of total damage done by that skill. if you have a BA this can be read off from the BA.
- adjust burst_frac to be the fraction of that skill's damage done while legacy is active. This can be tricky to estimate and
even harder to actually measure. I have included estimated amounts for full rotations, culverts, and burst (e.g. kalos, so 
35-40s) BAs. They might not be perfect but they are probably close enough. If you want something burstier than culvert but
less bursty than a burst BA, go like halfway between what I've listed for culvert and burst, idk we're getting into full
guesstimation territory at that point, it's very situation dependent.

Note that if your ba_percents don't add up to 100 (or close) it prints out a warning, but still runs. The values will get
normalized so they add to 100 no matter what. This can be handy if you want to fudge with some numbers without having to
manually adjust the ba_percent for every skill, but it can lead to misleading results if done by mistake (hence the warning).
"""
skills_input = {
    'infinity': {'ba_percent': 16.59, 'burst_frac': 1}, # burst_frac - 1 always
    'decree': {'ba_percent': 16.38, 'burst_frac': 0.4}, # burst_frac - full rot: 0.28, culvert: 0.4, burst: 0.95
    'shardbreaker': {'ba_percent': 14.89, 'burst_frac': 0.7}, # burst_frac - full rot: 0.45, culvert: 0.5 with cd hat, 0.7 w/o, burst: 1
    'cleave': {'ba_percent': 8.35, 'burst_frac': 0.3}, # burst_frac - full rot: 0.2, culvert: 0.3, burst: 0.95
    'storm': {'ba_percent': 7.02, 'burst_frac': 0.75}, # burst_frac - full rot: 0.75, culvert: 0.75, burst: 1
    'forge': {'ba_percent': 6.17, 'burst_frac': 0.3}, # burst_frac - full rot: 0.2, culvert: 0.3, burst: 0.95
    'bloom': {'ba_percent': 4.80, 'burst_frac': 0.35}, # burst_frac - full rot: 0.22, culvert: 0.35, burst: 0.9
    'dispatch': {'ba_percent': 4.77, 'burst_frac': 0.3}, # burst_frac - full rot: 0.2, culvert: 0.3, burst: 0.95
    'ruin': {'ba_percent': 4.40, 'burst_frac': 0.7}, # burst_frac - full rot: 0.45, culvert: 0.5 with cd hat, 0.7 w/o, burst: 1
    'reign': {'ba_percent': 3.42, 'burst_frac': 0.35}, # burst_frac - full rot: 0.25, culvert: 0.35, burst: 0.9
    'summons': {'ba_percent': 2.53, 'burst_frac': 0.35}, # burst_frac - full rot: 0.22, culvert: 0.35, burst: 0.9
    'rush': {'ba_percent': 2.40, 'burst_frac': 0.2}, # burst_frac - full rot: 0.18, culvert: 0.2, burst: 1
    'arachnid': {'ba_percent': 1.55, 'burst_frac': 0.5}, # burst_frac - full rot: 0.9, culvert: 0.5, burst: 0.9
    'solar crest': {'ba_percent': 1.50, 'burst_frac': 0.5}, # burst_frac - full rot: 0.9, culvert: 0.5, burst: 0.9
    'weapon aura': {'ba_percent': 1.49, 'burst_frac': 0.3}, # burst_frac - full rot: 0.2, culvert: 0.3, burst: 0.9
    'legacy': {'ba_percent': 1.08, 'burst_frac': 1}, # burst_frac - 1 always
    'plummet': {'ba_percent': 0.92, 'burst_frac': 0.1}, # burst_frac - full rot: 0.1, culvert: 0.1, burst: 0.1
    'conversion overdrive': {'ba_percent': 0.91, 'burst_frac': 0.67}, # burst_frac - full rot: 0.67, culvert: 0.67, burst: 0.9
    'blade torrent': {'ba_percent': 0.61, 'burst_frac': 1}, # burst_frac - 1 always
    'grave': {'ba_percent': 0.12, 'burst_frac': 0}, # burst_frac - 0 always since you should mark before legacy
}

"""
origin_percent is the expected ba_percent for level 1 origin skill. By default it is equal to infinity's ba_percent,
which should be pretty accurate based off of kms BAs that I've seen, but you can manually adjust it if you wish. Note
it's not included in the 'adds to 100' check described above and will get normalized in with everything else.
"""
origin_percent = skills_input['infinity']['ba_percent']

"""
okay this like doesn't really affect much... but i'm putting it in here for completeness - i estimated the ratio
of enhanced cleaves to non-enhanced cleaves as like 1:9.5, assuming you're dispatching often. If you are a dispatch
hater (aka gigacringe lmao) then pump this to like 10.5. Idk this shouldn't actually affect the optimization that much
as long as you keep it to a reasonable value (higher than like 8 and lower than 11.5). Note it should never be above 11.5
as it's impossible to do that many cleaves between enhanced cleaves.
"""
enhanced_cleave_frequency = 9.5 # enhanced cleave is one in every <value> cleaves


# In[149]:


skills_input_sum = np.sum([skill['ba_percent'] for skill in skills_input.values()])
if abs(skills_input_sum-100) > 0.1:
    print(f'Warning! skills_input_sum is {skills_input_sum} when it should be close to 100.0 (unless you know what you\'re doing')
# else:
#     print(f'Total BA percent: {skills_input_sum}')


# In[150]:


skills = []
percents = []
burst_array = []
for key in skills_input.keys():
    skills.append(key)
    percents.append(skills_input[key]['ba_percent'])
    burst_array.append(skills_input[key]['burst_frac'])
skills.append('maestro')
percents.append(10.0)
burst_array.append(1)
burst_array = np.array(burst_array)


# In[151]:


percents = np.array(percents)
normed_percents = percents/np.sum(percents)
# print(len(skills), skills, normed_percents)


# In[152]:


origin_costs = [30, 35, 40, 45, 50, 55, 60, 65, 200, 80, 90, 100, 110, 120, 130, 140, 150, 160, 350, 170, 180, 190, 200, 210, 220, 230, 240, 250, 500]
fourth_costs = [50, 15, 18, 20, 23, 25, 28, 30, 33, 100, 40, 45, 50, 55, 60, 65, 70, 75, 80, 175, 85, 90, 95, 100, 105, 110, 115, 120, 125, 250]
fifth_costs = [75, 23, 27, 30, 34, 38, 42, 45, 49, 150, 60, 68, 75, 83, 90, 98, 105, 113, 120, 263, 128, 135, 143, 150, 158, 165, 173, 180, 188, 375]


# In[153]:


# len(origin_costs), len(fourth_costs), len(fifth_costs)


# In[154]:


# burst_array = np.array([1, 0.28, 0.45, 0.2, 0.75, 0.18, 0.22, 0.2, 0.45, 0.25, 0.22, 0.18, 0.8, 0.8, 0.16, 1, 0.1, 0.67, 1, 0, 1])
# print(len(burst_array))
# burst_array = np.ones(21)
def get_burst_frac(current_percents):
    # burst_array currently is an estimate for full rotations - will result in undervaluing legacy in burstier scenarios
    return np.sum(current_percents*burst_array)

def norm(current_percents):
    return current_percents/np.sum(current_percents)


# In[155]:


# boostable things: origin, infinity, legacy, ruin, storm, cleave

fifth_enhancements = [11, 12, 13, 14, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 60]
origin_skill_percent = [3300*60+3900*140+skill_level*(110*60+130*140) for skill_level in range(1, 31)]
legacy_enhancement = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10]
cleave_enhancement = [(390+skill_level*12)*6 for skill_level in range(1, 31)]
enhanced_cleave_enhancement = [(300 + skill_level*9)*7*3 for skill_level in range(1, 31)]
dispatch_enhancement = [(480 + skill_level*8)*15 for skill_level in range(1, 31)]

# def infinity_boost(current_percents, infinity_level):
#     if infinity_level >= 30:
#         return 0
#     elif infinity_level == 0:
#         infinity_fd_gain = (100+fifth_enhancements[infinity_level])/100
#     else:
#         infinity_fd_gain = (100+fifth_enhancements[infinity_level])/(100+fifth_enhancements[infinity_level-1])
#     current_infinity_percent = current_percents[skills.index('infinity')]
#     return current_infinity_percent*infinity_fd_gain-current_infinity_percent   
# # print(infinity_boost(normed_percents, 29))

def fifth_boost(current_percents, fifth_level, skill_name):
    if fifth_level >= 30:
        return 0
    elif fifth_level == 0:
        fifth_fd_gain = (100+fifth_enhancements[fifth_level])/100
    else:
        fifth_fd_gain = (100+fifth_enhancements[fifth_level])/(100+fifth_enhancements[fifth_level-1])
    current_fifth_percent = current_percents[skills.index(skill_name)]
    return current_fifth_percent*fifth_fd_gain-current_fifth_percent   
# print(fifth_boost(normed_percents, 29, 'storm'))

def origin_boost(current_percents, origin_level):
    if origin_level >= 30:
        return 0
    origin_fd_gain = origin_skill_percent[origin_level]/origin_skill_percent[origin_level-1]
    current_origin_percent = current_percents[skills.index('maestro')]
    return current_origin_percent*origin_fd_gain-current_origin_percent
# print(origin_boost(normed_percents, 29))

def legacy_boost(current_percents, legacy_level):
    if legacy_level >= 30:
        return 0
    elif legacy_level == 0:
        burst_fd_bonus = 1.01
    else:
        burst_fd_bonus = (100+legacy_enhancement[legacy_level])/(100+legacy_enhancement[legacy_level-1])
    burst_frac = get_burst_frac(current_percents)
    burst_fd_increase = burst_fd_bonus*burst_frac-burst_frac
    
    actual_legacy_fd_gain = fifth_boost(current_percents, legacy_level, 'legacy')
    
    return burst_fd_increase+actual_legacy_fd_gain
# print(legacy_boost(normed_percents, 0))

def fourth_boost(current_percents, fourth_level):
    if fourth_level >= 30:
        return 0, 0
    elif fourth_level == 0:
        cleave_fd_bonus = cleave_enhancement[fourth_level]/(375*6)
        enhanced_cleave_fd_bonus = enhanced_cleave_enhancement[fourth_level]/(375*6)
        dispatch_fd_bonus = dispatch_enhancement[fourth_level]/(450*3*5)
    else:
        cleave_fd_bonus = cleave_enhancement[fourth_level]/cleave_enhancement[fourth_level-1]
        enhanced_cleave_fd_bonus = enhanced_cleave_enhancement[fourth_level]/enhanced_cleave_enhancement[fourth_level-1]
        dispatch_fd_bonus = dispatch_enhancement[fourth_level]/dispatch_enhancement[fourth_level-1]
        
    cleave_total_fd = 1/enhanced_cleave_frequency*enhanced_cleave_fd_bonus + (enhanced_cleave_frequency-1)/enhanced_cleave_frequency*cleave_fd_bonus
    current_cleave_percent = current_percents[skills.index('cleave')]
    current_dispath_percent = current_percents[skills.index('dispatch')]
    return current_cleave_percent*cleave_total_fd-current_cleave_percent, current_dispath_percent*dispatch_fd_bonus-current_dispath_percent
# print(fourth_boost(normed_percents, 0))


# In[156]:


lookahead = 10
def find_next_boost(current_percents, current_levels, lookahead=lookahead):
    efficiencies = np.zeros(6)
    fd_gains = np.zeros(6)
    extra_fd = 0 # used when dispatch matters
    
    origin_efficiencies = []
    origin_fd_increase = 0
    origin_cost = 0
    for i in range(lookahead):
        origin_fd_increase += origin_boost(current_percents, current_levels[0]+i)
        if i == 0:
            fd_gains[0] = origin_fd_increase
        origin_cost += origin_costs[current_levels[0]+i]
        origin_efficiencies.append(origin_fd_increase/origin_cost)
    efficiencies[0] = max(origin_efficiencies)
    
    for j, skill in enumerate(boostable_skills[1:4]):
        skill_efficiencies = []
        skill_fd_increase = 0
        skill_cost = 0
        for i in range(lookahead):
            skill_fd_increase += fifth_boost(current_percents, current_levels[j+1]+i, skill)
            if i == 0:
                fd_gains[j+1] = skill_fd_increase
            skill_cost += fifth_costs[current_levels[j+1]+i]
            skill_efficiencies.append(skill_fd_increase/skill_cost)
        efficiencies[j+1] = max(skill_efficiencies)
    
    legacy_efficiencies = []
    legacy_fd_increase = 0
    legacy_cost = 0
    for i in range(lookahead):
        legacy_fd_increase += legacy_boost(current_percents, current_levels[4]+i)
        if i == 0:
            fd_gains[4] = legacy_fd_increase
        legacy_cost += fifth_costs[current_levels[4]+i]
        legacy_efficiencies.append(legacy_fd_increase/legacy_cost)
    efficiencies[4] = max(legacy_efficiencies)
    
    cleave_efficiencies = []
    fourth_fd_increase = 0
    cleave_cost = 0
    for i in range(lookahead):
        cleave_fd_increase, dispatch_fd_increase = fourth_boost(current_percents, current_levels[5]+i)
        fourth_fd_increase += cleave_fd_increase + dispatch_fd_increase
        if i == 0:
            fd_gains[5] = cleave_fd_increase
            extra_fd = dispatch_fd_increase
        cleave_cost += fourth_costs[current_levels[5]+i]
        cleave_efficiencies.append(fourth_fd_increase/cleave_cost)
    efficiencies[5] = max(cleave_efficiencies)
    
    pick = np.argmax(efficiencies)
    
    if pick != 5:
        extra_fd = 0
    
    return pick, fd_gains[pick], extra_fd, efficiencies[pick]
    
origin_costs.extend(list(np.ones(lookahead+1)*1000))
fifth_costs.extend(list(np.ones(lookahead+1)*1000))
fourth_costs.extend(list(np.ones(lookahead+1)*1000))


# In[157]:


boostable_skills = ['maestro', 'infinity', 'storm', 'ruin', 'legacy', 'cleave']
current_levels = np.array([1, 0, 0, 0, 0, 0], dtype=int)
current_percents = normed_percents
# boostable_skills[1:4]


# In[158]:


print('skill\t\tlevel\t\tefficiency*\tfd gain')
print('--------------------------------------------------------------------')
while current_levels.min() < 30:
    arg_boost, fd_gain, extra_fd, efficiency = find_next_boost(current_percents, current_levels)
    
    if boostable_skills[arg_boost] == 'cleave':
        print(f'{boostable_skills[arg_boost]}\t\t{current_levels[arg_boost]}->{current_levels[arg_boost]+1}\t\t{efficiency*100:0.6f}\t{fd_gain*100+extra_fd*100:0.3f}\t({fd_gain*100:0.3f} from cleave, {extra_fd*100:0.3f} from dispatch)')
        current_percents[skills.index('cleave')] += fd_gain
        current_percents[skills.index('dispatch')] += extra_fd
    elif boostable_skills[arg_boost] == 'legacy':
        actual_legacy_fd = fifth_boost(current_percents, current_levels[4], 'legacy')
        other_skill_gain = fd_gain-actual_legacy_fd
        print(f'{boostable_skills[arg_boost]}\t\t{current_levels[arg_boost]}->{current_levels[arg_boost]+1}\t\t{efficiency*100:0.6f}\t{fd_gain*100:0.3f}')#\t({other_skill_gain*100} from fd bonus, {actual_legacy_fd*100} from legacy damage)')
        burst_frac = get_burst_frac(current_percents)
        current_percents[skills.index('legacy')] += actual_legacy_fd
        burst_skill_boost = current_percents*burst_array
        current_percents += burst_skill_boost*other_skill_gain/burst_frac
    elif boostable_skills[arg_boost] == 'infinity':
        print(f'{boostable_skills[arg_boost]}\t{current_levels[arg_boost]}->{current_levels[arg_boost]+1}\t\t{efficiency*100:0.6f}\t{fd_gain*100:0.3f}')
        current_percents[skills.index(boostable_skills[arg_boost])] += fd_gain
    else:
        print(f'{boostable_skills[arg_boost]}\t\t{current_levels[arg_boost]}->{current_levels[arg_boost]+1}\t\t{efficiency*100:0.6f}\t{fd_gain*100:0.3f}')
        current_percents[skills.index(boostable_skills[arg_boost])] += fd_gain
    
    current_percents = norm(current_percents)
    current_levels[arg_boost] += 1
print('\n*efficiency is fd gain divided by fragment cost. Overall efficiency\nshould decrease as you move down the list. You may note a few times\nwhere this doesn\'t happens, specifically with legacy. This is because\nthe fd increase every 3 levels gets amoratized over the previous levels.\nSo you get situations where the efficiency increases as you get closer to\nthe breakpoint. This behavior is expected if slightly unintuitive.')


# In[ ]:





# In[ ]:




