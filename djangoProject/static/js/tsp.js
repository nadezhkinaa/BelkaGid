function tsp(matrix) {
    return initialSolution(matrix);
}

// Возвращает минимальную стоимость пути из current к следующему городу
const findMinCost = (current, visited, graph) => {
    // Хранит минимальную стоимость пути до каждого города
    const costs = [];

    // Перебираем все города
    for (let i = 0; i < graph.length; i++) {
        // Если город не посещен и есть путь из current к нему
        if (!visited[i] && graph[current][i] > 0) {
            costs.push({
                cost: graph[current][i],
                next: i
            });
        }
    }

    // Возвращаем город с минимальной стоимостью пути
    return costs.reduce((prev, curr) => prev.cost < curr.cost ? prev : curr);
};

// Возвращает начальное решение
const initialSolution = (graph) => {
    // Хранит посещенные города
    const visited = new Array(graph.length).fill(false);

    // Начинаем с первого города
    let current = 0;
    visited[current] = true;

    // Инициализируем путь
    const path = [current];

    // Посещаем все оставшиеся города
    for (let i = 0; i < graph.length - 1; i++) {
        // Находим следующий город с минимальной стоимостью пути
        const next = findMinCost(current, visited, graph);

        // Добавляем город в путь и помечаем его как посещенный
        path.push(next.next);
        visited[next.next] = true;

        // Обновляем текущий город
        current = next.next;
    }

    return path;
};