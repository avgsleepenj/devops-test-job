// Функция для применения фильтров
function applyFilters() {
    var name = $('#filter-name').val();
    var age = $('#filter-age').val();
    var breed = $('#filter-breed').val();
    var status = $('#filter-status').val();

    $.getJSON('/api/cats', {name: name, age: age, breed: breed, status: status }, function(data) {

        // Очистить текущее содержимое таблицы, кроме заголовка
        $('#pets-table tr:not(:first)').remove();

        // Генерация новых строк таблицы
        var rows = data.map(function(pet) {
            return `<tr>
                        <td>${pet.name}</td>
                        <td>${pet.age}</td>
                        <td>${pet.breed}</td>
                        <td><img src="${pet.photo}" height="400"></td>
                        <td>${pet.status}</td>
                    </tr>`;
        }).join('');
        
        // Добавление новых строк в таблицу
        $('#pets-table').append(rows);
    });
}

// Загрузка начальных данных
applyFilters();