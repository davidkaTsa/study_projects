import torch
import torch.nn as nn
import pandas
import numpy as np
import cv2 as cv
import sklearn
import sklearn.metrics as metrics
import os
import torchvision
import random
import imgaug.augmenters as iaa
import imageio
import imgaug as ia

# input images size 144*144 and normalized
class CNN(nn.Module):
    def __init__(self, sizeImg):
        super(CNN, self).__init__()
        self.inLinear = sizeImg
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=12, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=12, out_channels=24, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels=24, out_channels=24, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.fc1 = nn.Linear(24*self.inLinear, 2)

    def forward(self, input_tensor):
        output = self.conv1(input_tensor)
        output = self.conv2(output)
        output = self.conv3(output)
        size_out = list(output.size()[1:])
        output = output.view(-1, size_out[0] * size_out[1] * size_out[2])
        output = self.fc1(output)

        return output


# crop images and resize to size 144*144
def resizeImg(img):
    if img.shape[0] == img.shape[1]:
        img_resize = cv.resize(img, (144, 144), cv.INTER_NEAREST)

    else:
        h = img.shape[1] if img.shape[0] > img.shape[1] else img.shape[0]
        w = h

        x = img.shape[1]/2 - w/2
        y = img.shape[0]/2 - h/2

        crop_img = img[int(y):int(y+h), int(x):int(x+w)]

        img_resize = cv.resize(crop_img, (144, 144), cv.INTER_NEAREST)
    return img_resize


# get all images from dataset
def getAllImages():
    allImagesMarker = [(i, "mar") for i in os.listdir("/content/drive/MyDrive/Козин_Цатурян_Гребнев/Маркер")]
    allImagesMel = [(i, "mel") for i in os.listdir("/content/drive/MyDrive/Козин_Цатурян_Гребнев/Мел")]
    allImages = []
    allImages.extend(allImagesMarker)
    allImages.extend(allImagesMel)
    allImages = random.sample(allImages, 806)
    return allImages


# function for augmentation
def augmentation(nameImg):

    if nameImg[1] == "mar":
        img = cv.imread(cv.samples.findFile(f"/content/drive/MyDrive/Козин_Цатурян_Гребнев/Маркер/{nameImg[0]}"))

    else:
        img = cv.imread(cv.samples.findFile(f"/content/drive/MyDrive/Козин_Цатурян_Гребнев/Мел/{nameImg[0]}"))
    x = random.random()*1.3
    k = round(x + 0.4 if x <= 0.4 else x, 2)
    scale = iaa.Affine(scale={"x": k, "y": k})
    image_scale = scale(image=img)
    rotate = iaa.Affine(rotate=(40, 270))
    image_rotate = rotate(image=img)

    image_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    b,g,r=cv.split(img)

    image_gbr=cv.merge((g,b,r))

    image_brg=cv.merge((b,r,g))


    return [(image_scale, nameImg[1]), (image_rotate, nameImg[1]), (image_rgb, nameImg[1]), (image_gbr, nameImg[1]),(image_brg, nameImg[1])]


# resize images, transform to tensor and normalized
def TransformAndNormalize(nameImg, original = True):
    if original:
        if nameImg[1] == "mar":
            img = cv.imread(cv.samples.findFile(f"/content/drive/MyDrive/Козин_Цатурян_Гребнев/Маркер/{nameImg[0]}"))
            resizeImage = resizeImg(img)
        else:
            img = cv.imread(cv.samples.findFile(f"/content/drive/MyDrive/Козин_Цатурян_Гребнев/Мел/{nameImg[0]}"))
            resizeImage = resizeImg(img)
    else:
        if nameImg[1] == "mar":
            resizeImage = resizeImg(nameImg[0])
        else:
            resizeImage = resizeImg(nameImg[0])

    transformations = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    normalizeImg = np.array(transformations(resizeImage))
    return normalizeImg

# prepare images for training
readyImages = []
labels = []
allImages = getAllImages()
for i in allImages:
    augScale, augRotate, augRGB, augGBR, augBRG = augmentation(i)
    normalizeAndResizeScale = TransformAndNormalize(augScale, False)
    normalizeAndResizeRotate = TransformAndNormalize(augRotate, False)
    normalizeAndResizeRGB = TransformAndNormalize(augRGB, False)
    normalizeAndResizeGBR = TransformAndNormalize(augGBR, False)
    normalizeAndResizeBRG = TransformAndNormalize(augBRG, False)
    normalizeAndResizeOrig = TransformAndNormalize(i)
    if i[1] == "mar":
        labels.extend([0,0,0,0,0,0])
    else:
        labels.extend([1,1,1,1,1,1])
    readyImages.extend([normalizeAndResizeOrig, normalizeAndResizeScale, normalizeAndResizeRotate, normalizeAndResizeRGB, normalizeAndResizeGBR, normalizeAndResizeBRG])


readyImagesTensor = torch.from_numpy(np.array(readyImages)).float()
labels = torch.from_numpy(np.array(labels)).long()


imagesTrain = readyImagesTensor[:int(len(readyImagesTensor)*0.8)]
labelsTrain = labels[:int(len(labels)*0.8)]

imagesTest = readyImagesTensor[int(len(readyImages)*0.8):]
labelsTest = labels[int(len(labels)*0.8):]


cnnFirst = CNN(18*18)

loss_func = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(cnnFirst.parameters(), lr=0.001)
epoch = 20
batch_size = 100

for i in range(epoch):
    for j in range(len(imagesTrain))[::batch_size]:
        optimizer.zero_grad()
        y_pred = cnnFirst(imagesTrain[j:j + batch_size])
        loss = loss_func(y_pred, labelsTrain[j: j + batch_size])
        loss.backward()
        optimizer.step()
    print(loss)

y_pred = cnnFirst(imagesTest)
loss = loss_func(y_pred, labelsTest)
y_pred = np.argmax(y_pred.detach().numpy(), axis = 1)
metrics.accuracy_score(labelsTest, y_pred)

# load weights for model
model = CNN(18*18)
path = "./Desktop/2CNNClassification.pth"
model.load_state_dict(torch.load(path))