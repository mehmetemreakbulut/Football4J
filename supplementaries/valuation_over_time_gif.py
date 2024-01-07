import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

data = pd.read_csv('./valuationoveryear.csv') 

fig, ax = plt.subplots()

def animate(i):
    ax.clear()
    ax.plot(data['year'][:i], data['totalValuation'][:i])
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Valuation')
    ax.set_title('Valuation Over Time')

ani = animation.FuncAnimation(fig, animate, frames=len(data), interval=500)

ani.save('valuation_animation_year.gif', writer='imagemagick')
