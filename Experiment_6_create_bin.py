import numpy as np
import math
import tqdm
import struct
import matplotlib.pyplot as plt
import csv


def create_moving_bar_1d(dimension=216,
                         polarity="bright",
                         direction='right',
                         bar_width=11,
                         background=0.5,
                         contrast=0.3):
    """
    :param dimension: the size of the frames in the sequence. Gives the number of possible positions of the bar.
    :param polarity: str. Whether the bar is "bright" or "dark" over a grey background.
    :param direction: the direction the bar is moving towards. 'right' or 'left'
    :param bar_width: int. The value should be an odd number
    :param background: float, between 0 and 1. The value of the frames background.
    :param contrast: float, between 0 and 1. The contrast between the background and the bar.
    :return: sequence. numpy array. The sequence of frames.
    """

    nb_frames = dimension
    assert bar_width%2 == 1, "The value of bar_width should be an odd number"
    half_width = int((bar_width - 1) / 2)
    if polarity == "bright":
        polarity_multiplicator = 1
    elif polarity == "dark":
        polarity_multiplicator = -1

    sequence = np.empty((nb_frames, dimension))
    black_frame = background * np.ones(dimension)

    for frame_nb in range(0, nb_frames):
        if direction == "right":
            center_position = frame_nb
        elif direction == "left":
            center_position = nb_frames - frame_nb

        if center_position - half_width >= 0:
            left_position = center_position - half_width
        else:
            left_position = 0

        if center_position + half_width <= dimension:
            right_position = center_position + half_width +1
        else:
            right_position = dimension +1

        sequence[frame_nb] = black_frame.copy()
        sequence[frame_nb, left_position:right_position] += polarity_multiplicator * contrast

    return sequence

def upscale_sequence(sequence, new_y_dimension):
    """ Upscales a 2d frame along the y axis
    The new y dimension should be a multiple of the original sequence y dimension.
    :param sequence: the sequence to be upscaled
    :param new_y_dimension: the y dimension of the output
    :return:
    """
    ratio = int(new_y_dimension/sequence.shape[1])
    assert type(ratio) is int, "The ratio of the original and new y dimension should be an integer"
    upscaled_frame = np.kron(sequence, np.ones((1,ratio)))
    return upscaled_frame

def create_perturbation_1d(seed=0, nb_frames = 50, dimension=216):
    """

    :param seed: the seed used for the random generation. Is also used to give an ID to the sequence.
    :param nb_frames: the number of perturbation frames.
    :param dimension: the number of checks/stripes in the perturbation.
    :return: perturbation. numpy array. The perturbation sequence. The values are -1 or 1.
    """
    np.seed = seed
    perturbation = np.random.choice([-1, 1], size=(nb_frames, dimension))
    return perturbation

def turn_1d_to_2d_frame(frames_1d):
    """ Turn a sequence of 1D frames (so a 2d array), into a sequence of 2D frames (so a 3D array).
    The values on the second axis (space) are repeated on the 3rd new axis, as to form stripes.
    :param frames_1d: The frames to transform
    :return:
    """
    frames_2d = np.repeat(frames_1d[:, :, np.newaxis], frames_1d.shape[1], axis=2)
    return frames_2d


def write_bin_file(filename, nbTotalFrames):
    TotalX = 864
    TotalY = 864
    nbTotalFrames = nbTotalFrames
    nBit = 8
    with open("{}.bin".format(filename), "wb") as fb:
        fb.write(struct.pack("H", TotalX))
        fb.write(struct.pack("H", TotalY))
        fb.write(struct.pack("H", nbTotalFrames))
        fb.write(struct.pack("H", nBit))


def randomize_stimulus(nb_sequences=40, nb_repetitions=30):
    """Creates a randomized sequence of repeated sequences.
    Sequences are identified by integers ranging from 1 to the number of sequences.
    
    """
    ordered_sequences = np.array([i for i in range(1, nb_sequences + 1)])
    repeated_sequences = np.tile(ordered_sequences, nb_repetitions)
    randomized_sequences = np.random.permutation(repeated_sequences)
    return randomized_sequences

# Set the following the following to True or False to perform them or not.
# Helps to break down the stimulus generation pipeline and do sanity checks.
# To do sanity checks, use the dedicated notebook.

root_dimension = 864

step_1 = True       # Generate the moving bar sequences, save as npy files
step_1_parameters = {'dimension': 144,      # The number of bar positions.
                    'background': 0.5,      # The intensity of the background
                    'contrast': 0.25,       # The contrast of the bar with the background (value added or substracted to the background)
                    'polarities': ["bright", "dark"],      # Whether the bar is brighter or darker than the background
                    'directions': ["right", "left"],       # The direction the moving bar moves towards
                    'bar_width': 7                         # The bar width, in bar positions.
                     }

step_2 = True     # Generate the perturbation sequences, save as npy files
step_2_parameters = {'dimension': 48,       # The number ot checks/stripes in the perturbation.
                     'nb_frames': step_1_parameters['dimension'],   # There are as many perturbation frames as positions of the moving bar
                     'seeds': list(range(1,2001))       # The seed used for the random generation process. Also used to give an ID to the perturbation sequence;
                     }



step_3 = True      # Assemble the perturbed moving bar sequences, save as npy files
step_3_parameters = {'dimension': 144,          # The dimension of one perturbed frame
                    'polarities': ["bright"],   # Whether the moving bar is brighter or darker than the background.
                    'directions': ["right", "left"],     # The direction the moving bar moves towards
                    'seeds': list(range(1,2001)),             # The seed used for the random generation process of the perturbation sequence
                    'perturbation_ratios':[0,0.6]   # The ration used to perturb the moving bar with the perturbation sequence
                     }



step_4 = True      # Load, correct, and save the sequences to a bin file.
substep_1 = False      # Load perturbed moving bar sequences (npy files)
substep_2 = False      # Reverse polarity. Save sanity checks.
substep_3 = False      # Flip frames for stimulus registration. Save sanity checks.
substep_4 = False      # Upscale the frames to the root dimension. Save sanity checks.
substep_5 = False      # Write the sequences to the bin file.



# Step 1: Generate the moving bar sequences, and save them as .npy files
if step_1:
    for polarity in step_1_parameters['polarities']:
        for direction in step_1_parameters['directions']:
            moving_bar = create_moving_bar_1d(polarity=polarity,
                                              direction=direction,
                                              dimension=step_1_parameters['dimension'],
                                              bar_width=step_1_parameters['bar_width'],
                                              background=step_1_parameters['background'],
                                              contrast=step_1_parameters['contrast']
                                              )

            np.save("./files/Moving_bar_{}_moving_{}".format(polarity, direction), moving_bar)
            print("Saved file: Moving_bar_{}_moving_{}.npy".format(polarity, direction))

# Step 2: Generate the perturbation sequences, and save them as .npy files
if step_2:
    for seed in step_2_parameters['seeds']:
        perturbation = create_perturbation_1d(seed=seed,
                                              nb_frames=step_2_parameters['nb_frames'],
                                              dimension=step_2_parameters['dimension'])
        np.save("./files/Perturbation_{}".format(seed), perturbation)
        print("Saved file: Perturbation_{}.npy".format(seed))

# Step 3: Assemble the perturbed moving bar sequences, and save them as .npy files
if step_3:
    for polarity in step_3_parameters['polarities']:
        for direction in step_3_parameters['directions']:
            for ratio in step_3_parameters['perturbation_ratios']:
                for seed in step_3_parameters['seeds']:

                    moving_bar = np.load("./files/Moving_bar_{}_moving_{}.npy".format(polarity, direction))
                    perturbation_sequence = np.load("./files/Perturbation_{}.npy".format(seed))
                    upscaled_perturbation = upscale_sequence(perturbation_sequence, moving_bar.shape[1])
                    print(upscaled_perturbation.shape)
                    perturbed_moving_bar = moving_bar + step_1_parameters['contrast'] * ratio * upscaled_perturbation

                    file_save_name = "./files/Perturbed_moving_bar_{}_moving_{}_perturbation_{}_ratio_{}.npy".format(polarity,
                                                                                                    direction,
                                                                                                    seed,
                                                                                                    ratio
                                                                                                    )
                    np.save(file_save_name, perturbed_moving_bar)
                    print("Assembled perturbed sequence and saved as file: {}".format(file_save_name))

# Write the perturbed moving bar sequences in a .bin file
if step_4:
    file_name = "Experiment_6_bright"
    nb_sequences = 200
    TotalX = root_dimension
    TotalY = root_dimension
    nBit = 8
    filenames = []

    with open("/media/thomas/TBT MAIN 3/{}.bin".format(file_name), "wb") as fb:
        fb.write(struct.pack("H", TotalX))
        fb.write(struct.pack("H", TotalY))
        fb.write(struct.pack("H", int(nb_sequences * step_1_parameters['dimension'])))
        fb.write(struct.pack("H", nBit))

        for polarity in step_3_parameters['polarities']:
            for direction in step_3_parameters['directions']:
                for ratio in step_3_parameters['perturbation_ratios']:
                    if ratio == 0:
                        file_load_name = "./files/Moving_bar_{}_moving_{}.npy".format(polarity, direction)
                        filenames += [file_load_name]
                        sequence = np.load(file_load_name)
                        print("Loaded file: {}".format(file_load_name))

                        # Reverse polarity
                        #sequence = 1 - sequence
                        # Scale values to 0-255
                        sequence = (sequence * 255).astype('uint8')
                        # Upscale dimension to root dimension
                        sequence = upscale_sequence(sequence, TotalY)
                        # Turn to 2D frames
                        sequence = turn_1d_to_2d_frame(sequence)
                        # Flip array
                        # sequence = np.rot90(sequence, k=2, axes=(1, 2))

                        sequence = sequence.astype('uint8')
                        frame_bytes = sequence.tobytes()
                        fb.write(frame_bytes)
                        fb.flush()



                    else:
                        for seed in step_3_parameters['seeds']:

                            file_load_name = "./files/Perturbed_moving_bar_{}_moving_{}_perturbation_{}_ratio_{}.npy".format(polarity,
                                                                                                        direction,
                                                                                                        seed,
                                                                                                        ratio
                                                                                                        )
                            filenames += [file_load_name]
                            sequence = np.load(file_load_name)
                            print("Loaded file: {}".format(file_load_name))

                            # Reverse polarity
                            # sequence = 1 - sequence
                            # Scale values to 0-255
                            sequence = (sequence * 255).astype('uint8')
                            # Upscale dimension to root dimension
                            sequence = upscale_sequence(sequence, TotalY)
                            # Turn to 2D frames
                            sequence = turn_1d_to_2d_frame(sequence)
                            # Flip array
                            # sequence = np.rot90(sequence, k=2, axes=(1,2))

                            sequence = sequence.astype('uint8')
                            frame_bytes = sequence.tobytes()
                            fb.write(frame_bytes)
                            fb.flush()