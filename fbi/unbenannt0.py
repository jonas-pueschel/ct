try:
    import matplotlib.pyplot as plt
    
    import numpy as np
    
    
    x = np.linspace(0.0, 5.0, 501)
    
    fig, ((ax1, ax2),(ax3,ax4)) = plt.subplots(2, 2, constrained_layout=True, sharey=True)
    ax1.plot(x, np.cos(6*x) * np.exp(-x))
    ax1.set_title('damped')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('amplitude')
    
    ax2.plot(x, np.cos(6*x))
    ax2.set_xlabel('time (s)')
    ax2.set_title('undamped')
    
    ax3.plot(x, np.cos(6*x) * np.exp(-x))
    ax3.set_title('damped')
    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('amplitude')
    
    ax4.plot(x, np.cos(6*x))
    ax4.set_xlabel('time (s)')
    ax4.set_title('undamped')
    
    
    fig.suptitle('Different types of oscillations', fontsize=16)
    fig.show()
except Exception as e:
    print(e)
   
input()