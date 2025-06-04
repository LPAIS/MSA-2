import os
from PIL import Image
import torch
from torch.utils.data import Dataset

class GlyphDataset(Dataset):
    def __init__(self, txt_path, clip_preprocess):
        """
        Args:
            txt_path (str): Path to the txt file listing image paths.
            clip_preprocess (callable): The preprocessing transform from CLIP.
        """
        self.image_paths = []
        self.labels = []
        self.char2idx = {}
        self.idx2char = []
        self.char_counts = {}
        
        # Read all image paths
        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        # Build mappings and lists
        for path in lines:
            # Extract character from filename (assuming format ".../<char>.png")
            char = os.path.splitext(os.path.basename(path))[0]
            if char not in self.char2idx:
                # Assign new index to new character
                self.char2idx[char] = len(self.idx2char)
                self.idx2char.append(char)
                self.char_counts[char] = 0
            self.char_counts[char] += 1
            self.image_paths.append(path)
            self.labels.append(self.char2idx[char])
        
        self.preprocess = clip_preprocess  # CLIP image preprocessing transform
        self.num_chars = len(self.idx2char)
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, index):
        img_path = self.image_paths[index]
        label = self.labels[index]            # numeric label for the character
        # Load image and apply CLIP preprocessing
        image = Image.open(img_path).convert("RGB")
        image_tensor = self.preprocess(image)  # yields a normalized tensor
        return image_tensor, label
