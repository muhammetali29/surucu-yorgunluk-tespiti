import cv2
import torch
import torchvision.transforms as transforms
from timm import create_model
import numpy as np
from PIL import Image
import winsound 

# LeViTModel adında özel bir PyTorch modeli tanımlanıyor
class LeViTModel(torch.nn.Module):
    def __init__(self, num_classes):

# torch.nn.Module yapısını miras alıyor (derin öğrenme model sınıfı)

        super(LeViTModel, self).__init__()
        # 'levit_384' isimli LeViT modeli oluşturuluyor
        # pretrained=False → hazır ağırlıklar yüklenmesin
        # num_classes → kaç sınıfa ayrım yapılacak (bu projede 2: yorgun / normal)
        self.backbone = create_model('levit_384', pretrained=False, num_classes=num_classes)

    def forward(self, x):
        # Modelin ileri besleme (forward) işlemi tanımlanıyor
        # x → giriş tensörü, çıktı olarak sınıf tahmini döner
        return self.backbone(x)
    # Modelin eğitilmiş ağırlık dosyasının yolu belirtiliyor
model_path = "levit_model_fold_3.pth"

# Modelin kaç sınıfı ayırt edeceği belirtiliyor (0: normal, 1: yorgun)
num_classes = 2
# LeViT model nesnesi oluşturuluyor, çıkış katmanı 2 sınıflı olacak şekilde ayarlanıyor
model = LeViTModel(num_classes=num_classes)
# Eğitilmiş model ağırlıkları .pth dosyasından yükleniyor, CPU’da çalışacak şekilde ayarlanıyor
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
# Model tahmin moduna alınıyor (eval = sadece tahmin yap, eğitim yapma)
model.eval()

# Kamera görüntüsünü modele uygun hale getirmek için yeniden boyutlandırır, tensöre çevirir ve normalize eder

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

cap = cv2.VideoCapture(0)  #0 bilgisayar kamerası 1 telefon kamerası

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera görüntüsü alınamadı!")
        break

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    input_tensor = transform(img).unsqueeze(0) 

    with torch.no_grad():
        output = model(input_tensor)
        prediction = torch.argmax(output, dim=1).item()

    if prediction == 1: 
        cv2.putText(frame, "", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        winsound.Beep(1000, 500)  
    else:  
        cv2.putText(frame, "NORMAL", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
