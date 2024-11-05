import pandas as pd
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.pyplot as plt

"""
2 plots horizontal
"""
fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(1, 2)
gs.update(wspace=0.1, hspace=0.35)

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.ylabel('Fill Me In')

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/gridspec_templates/Two_horizontal.png',
            dpi=300, bbox_inches="tight")
plt.close()


"""
2 plots vertical
"""
fig = plt.figure(figsize=(8, 16))
gs = gridspec.GridSpec(2, 1)
gs.update(wspace=0.1, hspace=0.1)

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xticks([])
plt.ylabel('Fill Me In')

# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.ylabel('Fill Me In')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/gridspec_templates/Two_vertl.png',
            dpi=300, bbox_inches="tight")
plt.close()



"""
4 plots horizontal
"""
fig = plt.figure(figsize=(32, 8))
gs = gridspec.GridSpec(1, 4)
gs.update(wspace=0.1, hspace=0.35)

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.ylabel('Fill Me In')

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])


# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 3:4])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])


plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/gridspec_templates/Four_horizontal.png',
            dpi=300, bbox_inches="tight")
plt.close()



"""
4x2 plots horizontal
"""
fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(2, 4)
gs.update(wspace=0.1, hspace=0.15)

# TOP ROW
# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.ylabel('Fill Me In')

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])


# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 3:4])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])

# BOTTOM ROW
# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.ylabel('Fill Me In')

# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])

# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 2:3])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])


# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 3:4])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])


plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/gridspec_templates/Fourx2.png',
            dpi=300, bbox_inches="tight")
plt.close()








"""
2x2 plots horizontal
"""
fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(2, 2)
gs.update(wspace=0.1, hspace=0.15)

# TOP ROW
# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.ylabel('Fill Me In')

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])

# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])


# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])


plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/gridspec_templates/2x2.png',
            dpi=300, bbox_inches="tight")
plt.close()




"""
3x2 plots horizontal
"""
fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(3, 2)
gs.update(wspace=0.1, hspace=0.15)

# TOP ROW
# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.ylabel('Fill Me In')

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])


# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])


# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])


# plot structure
xtr_subsplot = fig.add_subplot(gs[2:3, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])

# plot structure
xtr_subsplot = fig.add_subplot(gs[2:3, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])





plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/gridspec_templates/3x2.png',
            dpi=300, bbox_inches="tight")
plt.close()



"""
3x2 plots horizontal
"""
fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(2, 3)
gs.update(wspace=0.1, hspace=0.15)

# TOP ROW
# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.ylabel('Fill Me In')

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])

# BOTTOM ROW
# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.ylabel('Fill Me In')

# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 1:2])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])

# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 2:3])
# add what we're plotting
plt.scatter([1,2,3], [1,2,3])
# formatting
plt.xlabel('Fill Me In')
plt.yticks([])

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/gridspec_templates/3x2.png',
            dpi=300, bbox_inches="tight")
plt.close()
















