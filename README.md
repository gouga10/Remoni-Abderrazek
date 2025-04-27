# Python Script Launcher

This project provides a simple launcher that opens and runs two Python scripts (`server.py` and `Cloud_RealTime.py`) in separate terminal windows.

## Project Structure


## How It Works

- `launcher.py` uses `subprocess.Popen` to open two new terminal windows.
- Each terminal runs one of the two scripts:
  - `server.py`
  - `Cloud_RealTime.py`

## Requirements

- Python 3.x
- Windows OS (the `start`, `cmd`, and `/k` commands are Windows-specific)
  
Make sure you have Python added to your system `PATH`.

## How to Use

1. **Clone or download** this repository.
2. **Navigate** to the project directory.
3. **Run** the launcher script:

```bash
python launcher.py
```

--------------------------------------------------------------------------------------------------------------------------------------------------------------
To create a Tizen OS project targeting Galaxy Watch devices, start by opening the Tizen Studio and creating a new project.
Choose Tizen 7.0 (v7) as the platform version to ensure compatibility with the latest Galaxy Watch models.
 During project setup, select the Wearable profile and choose a template like Basic Watch App or Galaxy Watch App depending on your needs.
This will scaffold the project with the correct structure and permissions optimized for Galaxy Watch applications.
After setup, you can build, run, and deploy the app directly to an emulator or a connected Galaxy Watch device.

----------------------------------------------------------------------------------------------------------------------------------------------------------


In our work with vision-language models, we utilized three datasets.
The principal dataset is Toyota, where we conducted the fine-tuning of the LLaMA 3.2 Vision model and performed its evaluation.
This dataset served as the foundation for adapting the model to vision-language tasks.
Additionally, we used two other datasets, NTU and Upfall, specifically to evaluate the model's vision capabilities in the context of activity recognition.
These datasets helped assess how well the model can understand and interpret human actions from visual input.


For all_caps.json it contains the generations of the multiple VLMs on the toyota datset and it is organized as follows 


```bash
allcaps[image]=[ground_truth(activity name),llama,intern2kf,internVL_Vcaps,deepseek,captions(correct_caption)]
```







