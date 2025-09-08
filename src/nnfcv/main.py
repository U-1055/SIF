import os.path
import torchvision.transforms.v2
from torch import nn
import torch.nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from matplotlib import pyplot
from PIL import Image
import csv
from datetime import time, timedelta, datetime
#определение классов

letters_data = {
    '0': 'A',  '6': 'G',   '12': 'M',  '18': 'S',  '24': 'Y',
    '1': 'B',  '7': 'H',   '13': 'N',  '19': 'T',  '25': 'Z',
    '2': 'C',  '8': 'I',   '14': 'O',  '20': 'U',  '26': 'Не удалось распознать букву',
    '3': 'D',  '9': 'J',   '15': 'P',  '21': 'V',
    '4': 'E',  '10': 'K',  '16': 'Q',  '22': 'W',
    '5': 'F',  '11': 'L',  '17': 'R',  '23': 'X',

}

data_path = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
    )),
    'data', 'NN_data'
)

class MyDataset(Dataset): #класс, наследуемый от класса Dataset из PyTorch. Нужен для создания пользовательского набора данных

    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        """Метод инициализации, определяет путь к файлу аннотаций и папку с изображениями"""
        super().__init__()

        self.img_labels = annotations_file # путь к файлу с аннотациями
        self.img_dir = img_dir # папка с изображениями

    def __len__(self):
        """Возвращает количество образцов в наборе данных"""
        with open(self.img_labels, 'r') as labels:
            return len(labels.readlines())

    def __getitem__(self, idx):
        """Возвращает изображение и его метку в тензорном представлении"""

        to_dtype = torchvision.transforms.v2.ToDtype(torch.float32)
        tensor = torchvision.transforms.ToTensor()

        with open(self.img_labels, 'r') as labels:
            if idx == 0: idx = 1
            class_data = list(csv.reader(labels))


        image_name = class_data[idx][0]
        probabilities = []
        for i in range(1, 27):
            probabilities.append(int(class_data[idx][i]))
        probabilities.append(0) #для соответствия размерности выходного тензора сети и целевого тензора
        img_path = os.path.join(self.img_dir, image_name)

        image = Image.open(img_path)
        image = image.resize((160, 160))
        image = tensor(image)
        image = to_dtype(image)


        probabilities = torch.tensor(probabilities, dtype=torch.float32)

        return image, probabilities

class NN(nn.Module):
    """Класс, описыващий нейронную сеть"""
    def __init__(self):
        """Метод инициализации. nn.Flatten - класс для превращения n-мерного массива в одномерный"""
        super().__init__()

        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))

        self.layer2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))

        self.layer3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))

        self.drop_out = nn.Dropout()

        self.fc1 = nn.Linear(20 * 20 * 128, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 270)
        self.fc4 = nn.Linear(270, 27)

    def forward(self, x):

        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)

        if out.dim() == 4:
            out = out.reshape(out.size(0), -1)

        out = self.drop_out(out)

        out = self.fc1(out)
        out = self.fc2(out)
        out = self.fc3(out)
        out = self.fc4(out)

        return out

class NN_learning():

    def __init__(self):

        """Инициализирующий метод, объявляет пути к данным, классы наборов данных и их загрузчиков"""

        annotation_path_tr = os.path.join(data_path, 'Letters.v1i.multiclass', 'train', '_classes.csv')
        annotation_path_ts = os.path.join(data_path, 'Letters.v1i.multiclass', 'test', '_classes.csv')
        image_dir_tr = os.path.join(data_path, 'Letters.v1i.multiclass', 'train')
        image_dir_ts = os.path.join(data_path, 'Letters.v1i.multiclass', 'test')

        trans = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
        train_data = MyDataset(annotation_path_tr, image_dir_tr, trans)

        test_data = MyDataset(annotation_path_ts, image_dir_ts, trans)

        self.train_dataloader = DataLoader(train_data, batch_size=30, shuffle=True)
        self.test_dataloader = DataLoader(test_data, batch_size=7, shuffle=False)

        self.learning()

    def learning(self):
        """Метод для обучения нейронной сети. Объявляет гиперпараметры, производит вызов self.train_loop для
           тренировочного цикла и self.test_loop для тестового цикла"""

        model = NN()

        # гиперпараметры
        epochs = 5
        learning_rate = 1e-3
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        self.batch = 30
        loss_fn = nn.MSELoss()

        for i in range(epochs):
            self.train_loop(dataloader=self.train_dataloader, loss_fn=loss_fn, optimizer=optimizer, model=model)
            self.test_loop(dataloader=self.test_dataloader, loss_fn=loss_fn, model=model)

        #torch.save(model.state_dict(), 'model_weights.txt')
    def train_loop(self, dataloader, loss_fn, optimizer, model):
        """Тренировочный цикл, проходит по тренировочному набору данных, вычисляет функцию ошибки, строит её градиент и
           производит обратный проход через сеть для корректировки весовых коэффициентов"""
        t1 = datetime.now()

        size = len(dataloader.dataset) - 1
        true_predictions = 0
        i_complete = 0

        for i, (X, y) in enumerate(dataloader):

            if i == 67:
                break

            pred = model(X)
            loss = loss_fn(pred, y)

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            fact = torch.argmax(pred, 1)
            target = torch.argmax(y, 1)
            equal = torch.eq(fact, target)

            true_predictions += torch.count_nonzero(equal).item()
            i_complete += self.batch
            print(f'Время: {(datetime.now() - t1) // 30}')
            if i % 1 == 0:
                images = (i + 1) * self.batch
                print(f'{i + 1}. Ошибка:{round(loss.item(), 4)}|Пройдено:{images}/{size}|Точность: {round((true_predictions / i_complete) * 100, 2)}%')
                true_predictions = 0
                i_complete = 0

    def test_loop(self, dataloader, loss_fn, model):
        """Тестовый цикл. Проходит по тестовому набору данных, градиент функции ошибки не строит,
           вычисляет точность классификации объектов сети и функцию ошибки"""

        model.eval()

        num_batches = len(dataloader)
        test_loss, correct = 0, 0

        file = open('Документация_обучения.txt')
        with torch.no_grad():

            i = 0
            for X, y in dataloader:
                pred = model(X)
                test_loss += loss_fn(pred, y).item()

                fact = torch.argmax(pred, 1)
                target = torch.argmax(y, 1)
                equal = torch.eq(fact, target)

                correct += torch.count_nonzero(equal).item()
                i += 1

        test_loss /= num_batches
        correct /= 287

        with open('Документация_обучения.txt', 'a') as file:
            file.write(f"\nТестовый проход: \nТочность:{round(correct * 100, 2)}%, Ошибка: {round(test_loss, 4)} \n")

        print(f"\nТестовый проход: \nТочность:{round(correct * 100, 2)}%, Ошибка: {round(test_loss, 4)} \n")

        return (correct * 100, test_loss)

def define_image(image):
    """Функция для вызова из файла интерфейса, нормализует изображение и вводит его в нейронную сеть в виде тензора"""

    weights_path = os.path.join(data_path, 'model_weights.txt')

    to_dtype = torchvision.transforms.v2.ToDtype(torch.float32)
    tensor = torchvision.transforms.ToTensor()
    softmax = nn.Softmax(dim=1)
    model = NN()
    model.load_state_dict(torch.load(weights_path, weights_only=True))

    img = image.resize((160, 160))
    img = tensor(img)
    img = to_dtype(img)
    img = img[None]
    img.shape

    with torch.no_grad():

        model.eval()
        pred = model(img)
        pred = softmax(pred)
        time2 = datetime.now()

        return [letters_data[str(torch.argmax(pred).item())]] #ToDo: внимание, инетерфейс не будет работать т.к. функция возвращает только одно значение


if __name__ == '__main__':
    NN_learning()
