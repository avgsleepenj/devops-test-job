const form = document.querySelector('#filters');
const petsList = document.querySelector('#pets-list');
const statusBox = document.querySelector('#status');
const resultCount = document.querySelector('#result-count');

const placeholderImage = `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f3eee8"/>
  <text x="400" y="285" text-anchor="middle" font-size="84">🐾</text>
  <text x="400" y="365" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" fill="#6f6258">Фото скоро появится</text>
</svg>`)}`;

function ageLabel(age) {
    const lastTwo = age % 100;
    const last = age % 10;
    if (lastTwo >= 11 && lastTwo <= 14) return `${age} лет`;
    if (last === 1) return `${age} год`;
    if (last >= 2 && last <= 4) return `${age} года`;
    return `${age} лет`;
}

function createTextElement(tag, className, text) {
    const element = document.createElement(tag);
    element.className = className;
    element.textContent = text;
    return element;
}

function createPetCard(pet) {
    const article = document.createElement('article');
    article.className = 'pet-card';

    const imageWrapper = document.createElement('div');
    imageWrapper.className = 'pet-card__image-wrapper';

    const image = document.createElement('img');
    image.className = 'pet-card__image';
    image.src = pet.photo || placeholderImage;
    image.alt = `Кошка ${pet.name}`;
    image.loading = 'lazy';
    image.addEventListener('error', () => {
        image.src = placeholderImage;
        image.alt = `Фото кошки ${pet.name} недоступно`;
    }, { once: true });

    imageWrapper.append(image);

    const content = document.createElement('div');
    content.className = 'pet-card__content';

    const headingRow = document.createElement('div');
    headingRow.className = 'pet-card__heading';
    headingRow.append(
        createTextElement('h3', '', pet.name),
        createTextElement('span', 'badge', pet.status),
    );

    const details = document.createElement('dl');
    details.className = 'pet-card__details';

    [['Возраст', ageLabel(pet.age)], ['Порода', pet.breed]].forEach(([term, value]) => {
        const row = document.createElement('div');
        row.append(
            createTextElement('dt', '', term),
            createTextElement('dd', '', value),
        );
        details.append(row);
    });

    content.append(headingRow, details);
    article.append(imageWrapper, content);
    return article;
}

function updateCount(count) {
    const lastTwo = count % 100;
    const last = count % 10;
    let noun = 'питомцев';
    if (!(lastTwo >= 11 && lastTwo <= 14)) {
        if (last === 1) noun = 'питомец';
        else if (last >= 2 && last <= 4) noun = 'питомца';
    }
    resultCount.textContent = `Найдено: ${count} ${noun}`;
}

async function loadPets() {
    statusBox.hidden = false;
    statusBox.className = 'status';
    statusBox.textContent = 'Загружаем питомцев…';
    petsList.hidden = true;
    petsList.replaceChildren();
    resultCount.textContent = '';

    const params = new URLSearchParams();
    new FormData(form).forEach((value, key) => {
        const normalized = String(value).trim();
        if (normalized) params.set(key, normalized);
    });

    try {
        const query = params.toString();
        const response = await fetch(`/api/cats${query ? `?${query}` : ''}`, {
            headers: { Accept: 'application/json' },
        });
        const payload = await response.json();

        if (!response.ok) {
            throw new Error(payload.error || 'Не удалось загрузить данные');
        }

        updateCount(payload.length);

        if (payload.length === 0) {
            statusBox.textContent = 'По выбранным фильтрам никого не найдено. Попробуйте изменить запрос.';
            return;
        }

        const fragment = document.createDocumentFragment();
        payload.forEach((pet) => fragment.append(createPetCard(pet)));
        petsList.append(fragment);
        petsList.hidden = false;
        statusBox.hidden = true;
    } catch (error) {
        statusBox.className = 'status status--error';
        statusBox.textContent = `Ошибка: ${error.message}`;
    }
}

form.addEventListener('submit', (event) => {
    event.preventDefault();
    loadPets();
});

form.addEventListener('reset', () => {
    window.setTimeout(loadPets, 0);
});

loadPets();
