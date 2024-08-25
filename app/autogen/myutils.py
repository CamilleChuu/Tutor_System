import pickle , re, json

def get_user_input(state="You ( 'exit' to quit): "):
    user_input = input(state)
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        exit(0)  # Exit the program
    return user_input

def is_valid_num_input(user_input, range):
    try:
        number = int(user_input)
        return number in range
    except ValueError:
        return False
    
def update_chat_log(new_entity, log, dir):
    log.append(new_entity)
    with open(dir, 'wb') as f:
            pickle.dump(log, f)

def process_exp(_input):
        input = re.sub('\n', '', _input)
        input = re.findall('\{.*\}', input)[0]
        output = json.loads(input)
        return output

def induce_exp_idx(exp_log, exp_full):
    output = None
    for exp in exp_full:
          if exp not in exp_log:
               if output is None or int(exp) < int(output):
                    output = int(exp)
    return output

def show_image(image_path, image_title="Image Display"):
    import tkinter as tk
    from PIL import Image, ImageTk
    # Create a window
    window = tk.Tk()
    window.title(image_title)

    # Load an image using PIL
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    label = tk.Label(window, image=photo)
    label.image = photo  # keep a reference!
    label.pack()

    # Run the application
    window.mainloop()