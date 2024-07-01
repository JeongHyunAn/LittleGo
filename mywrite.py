#!/usr/bin/env python
# coding: utf-8

# In[1]:


def writeOutput(result):
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open('./output.txt', 'w') as f:
        f.write(res)

