# 🧊 Smart Fridge App – AI-Powered Food Freshness & Inventory Tracker

A mobile application that uses **AI** and **Computer Vision** to detect fruit freshness, extract expiry dates, and help track fridge inventory in real-time from a distance.

## 📱 Features

- 📸 Capture or upload images from phone
- 🍎 Predict **Fresh vs Rotten** using a **MobileNetV2** model
- 🧾 Read **Expiry Dates** from labels using **PaddleOCR**
- 🗃️ Store expiry dates locally with **AsyncStorage**
- 🗑️ Remove items from inventory when taken out of the fridge
- 🌐 Real-time **remote inventory monitoring**
- 📦 Future-ready: scalable with **Raspberry Pi + camera module**

## 🔧 Tech Stack

| Layer       | Technology          |
|-------------|---------------------|
| Frontend    | React Native CLI    |
| Backend     | Flask (Python)      |
| OCR Engine  | PaddleOCR           |
| ML Model    | MobileNetV2         |
| Storage     | AsyncStorage (React Native) |

## 🧠 Machine Learning

- **Model**: MobileNetV2-based CNN
- **Trained to classify**: Fresh vs Rotten fruits
- **Image Input Size**: 224x224 pixels

## 🧾 OCR (Expiry Date Reader)

- **OCR Framework**: [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- **Supports**: DDMMYY, DD/MM/YYYY, and other real-world printed formats
- **Preprocessing**: Histogram equalization for faint texts
- **Extracts only expiry dates** (not full text)

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js & npm
- Android Studio (for emulator/device testing)

### Clone the Repo

```bash
git clone https://github.com/shreya-024/Smart-Fridge-App
cd Smart-Fridge-App
