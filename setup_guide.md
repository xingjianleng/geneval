### Why?
The original `environment.yml` file is not compatible with H100 GPUs. So, I created this setup guide to help myself set up the environment correctly.

### 1. Create conda environment
```bash
conda create -n geneval python=3.8.10 -y
conda activate geneval
```

### 2. Clone the repository and download the detection model checkpoint
```bash
git clone https://github.com/xingjianleng/geneval.git
cd geneval

mkdir -p "<OBJECT_DETECTOR_FOLDER>/"
./evaluation/download_models.sh "<OBJECT_DETECTOR_FOLDER>/"
```

### 3. Install basic dependencies
```bash
pip install torch==2.1.2 torchvision==0.16.2
pip install open-clip-torch==2.26.1
pip install clip-benchmark==1.6.1
pip install einops==0.8.1
pip install lightning==2.3.3
pip install diffusers["torch"]==0.32.2
pip install transformers==4.46.3
pip install tomli==2.2.1
pip install platformdirs==4.3.6
pip install --upgrade setuptools==75.3.2
pip install pandas==1.5.3
pip install h5py==3.11.0
```

### 4. Install mmcv dependencies
This is the tricky part, because pre-built `mmcv` is not for H100 GPU with `sm90` CUDA computation capability. So, we need to build `mmcv` from source.

Before installing `mmcv`, make sure you have installed `cuda` binaries corresponding to your `torch cuda` version. Below is an example of how you can load the correct version from SLURM package manager.
```bash
module load cuda/12.1.0
``` 

```bash
TORCH_CUDA_ARCH_LIST=9.0 pip install mmengine mmcv-full==1.7.2
```

**P.S.** If you are using GPUs older than H100, simply remove the `TORCH_CUDA_ARCH_LIST=9.0` environment variable.

### 5. Install mmdetection dependencies
```bash
git clone https://github.com/open-mmlab/mmdetection.git
cd mmdetection; git checkout 2.x
pip install -v -e .
cd ..
```

### 6. Image generation and evaluation
Then, please follow the instructions in the `README.md` file to generate images and evaluate them.

### References
- [An improved guide for `geneval` environment setup](https://github.com/djghosh13/geneval/issues/12#issue-2727852470)
- [`mmcv` FAQ](https://github.com/open-mmlab/mmdetection/blob/master/docs/en/faq.md#pytorchcuda-environment)
