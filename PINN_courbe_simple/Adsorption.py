import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from io import BytesIO

from pinn import PINN

params_to_search = {
    # ["Hammersley", "LHS", "Halton", "pseudo", "Sobol", "uniform"]
    "train_distribution": ["uniform"],
    "num_domain": [5000],
    "num_boundary":[5000],
    "num_initial": [1000],
    "num_test": [1000],

    # ["Glorot normal", "Glorot uniform", "He normal", "He uniform", "LeCun normal", "LeCun uniform", "Orthogonal", "zeros"]
    "initializer": ["Glorot normal"],
    # [elu, relu, gelu, selu, sigmoid, silu, sin, silu, tanh]
    "activation": ["tanh"],
    "nb_couches": [8],
    "nb_neur_couche": [32],

    "maxcor": [100],
    "ftol": [0],
    "gtol": [1e-8],
    "maxiter": [15000],
    "maxfun": None,
    "maxls":  [100]
}

# Choix des paramètres parmi les valeurs porposées
current_params = {param: np.random.choice(values) if isinstance(values, list) else values for param, values in params_to_search.items()}

loss_weights = [1e2, 1e2, 1e5, 1e5, 1e4, 1e4]
loss_weights_lbfgs = [1e2, 1e2, 1e5, 1e5, 1e4, 1e4]



# Create an instance of PINN 
pinn_obj = PINN(
    x_start = 0, 
    x_end = 1, 
    time_start = 0, 
    time_end = 1, 
    total_points = 501,
    num_time_steps = 501,
    save_path=""
)


# Run the PINN
input, output, cs, cg, losshistory, train_state = pinn_obj.run(
    current_params = current_params, 
    loss_weights = loss_weights,
    loss_weights_lbfgs = loss_weights_lbfgs,
    iterations = 100
)

# Graphs ------------------------------------------------------------
cs = np.load('cs.npy')
cg = np.load('cg.npy')

cs_analytical = pd.read_csv('cs_analytical.csv', header=None)
cg_analytical = pd.read_csv('cg_analytical.csv', header=None)

# Convert DataFrame to arrays
cs_analytical = cs_analytical.values
cg_analytical = cg_analytical.values
x_start = 0
x_end = 1
time_start = 0
time_end = 1

total_points = len(cs[:,0])
num_time_steps = len(cs[0,:])
dt = time_end / num_time_steps
x = np.linspace(x_start, x_end, total_points)
t = np.linspace(time_start, time_end, num_time_steps)
X, T = np.meshgrid(x,t) 
input = np.hstack((X.flatten()[:,None], T.flatten()[:,None]))


### Post Processing
# Set up the figure and axis
fig, ax = plt.subplots(figsize=(4.5, 3.5))

# Create a list to store the generated frames
frames = []

# Loop through each timestep
for timestep in range(cs.shape[1]):
    # Clear the axis
    ax.clear()
    
    # Plot the water depth at the current timestep
    
    ax.plot(x, cs_analytical[:, timestep], label='Analytical')
    ax.plot(x, cs[:, timestep], linestyle='--', label='PINN')
    
    # Fill the area between the curves
    ax.fill_between(x, 0, cs[:, timestep], color='skyblue', alpha=0.5)
   # ax.fill_between(x, 0, h_values_transpose[:, timestep], color='lightgreen', alpha=0.5)
    
    timestamp = (timestep+1) * dt
    # Set the axis labels and title
    ax.set_xlabel('x-distance [m]')
    ax.set_ylabel('Concentration cs [g/mol]')
    ax.set_title(f'Time: {timestamp:.2f} s')
    ax.set_xlim([x_start, x_end])
    ax.set_ylim([0, 10.5])
    ax.legend()  # Add legend
    
    # Create an in-memory file object
    img_buffer = BytesIO()
    
    # Save the current figure to the in-memory file object
    plt.savefig(img_buffer, format='png')
    
    # Read the contents of the in-memory file object and add it to the list of frames
    img_buffer.seek(0)
    img_data = img_buffer.getvalue()
    img = imageio.imread(img_data, format='PNG')
    frames.append(img)
    
    # Clear the in-memory file object for the next iteration
    img_buffer.close()
    
# Save the list of frames as an MP4 file
# (adjust the file name and parameters as needed)
mp4_filename = 'C:/diskD/0 - POLYTECH/5A/COURS/PROJET INGE/Projet_ingenieur/water_depth_animation.mp4'
imageio.mimsave(mp4_filename, frames, fps=10)

# Show the final animation
plt.show()


#Plot for velocity

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(4.5, 3.5))

# Create a list to store the generated frames
frames = []

# Loop through each timestep
for timestep in range(cg.shape[1]):
    # Clear the axis
    ax.clear()
    
    # Plot the water depth at the current timestep
    
    ax.plot(x, cg_analytical[:, timestep], label='Analytical')
    ax.plot(x, cg[:, timestep], linestyle='--', label='PINN')
    
    timestamp = (timestep+1) * dt
    # Set the axis labels and title
    ax.set_xlabel('x-distance [m]')
    ax.set_ylabel('Concentration cg [g/mol]')
    ax.set_title(f'Time: {timestamp:.2f} s')
    ax.set_xlim([x_start, x_end])
    #ax.set_ylim([0.8*np.min(u_analytical), 1.2*np.max(u_analytical)])
    ax.set_ylim([0, 1.2])
    ax.legend()  # Add legend
    
    # Create an in-memory file object
    img_buffer = BytesIO()
    
    # Save the current figure to the in-memory file object
    plt.savefig(img_buffer, format='png')
    
    # Read the contents of the in-memory file object and add it to the list of frames
    img_buffer.seek(0)
    img_data = img_buffer.getvalue()
    img = imageio.imread(img_data, format='PNG')
    frames.append(img)
    
    # Clear the in-memory file object for the next iteration
    img_buffer.close()
    
# Save the list of frames as an MP4 file
# (adjust the file name and parameters as needed)
mp4_filename = 'C:/diskD/0 - POLYTECH/5A/COURS/PROJET INGE/Projet_ingenieur/water_velocity_animation.mp4'
imageio.mimsave(mp4_filename, frames, fps=10)

# Show the final animation
plt.show()



