function renderEgePage(main) {
    let html = '<div class="card"><h2>🎯 ЕГЭ-тренажёр</h2><p>Тренируйся выполнять задания из ЕГЭ</p></div>';
    EGE_TASKS.forEach(t => {
        html += '<div class="card" style="cursor:pointer;" onclick="startEgeTask(' + t.id + ')">' +
            '<h3>Задание ' + t.type + ': ' + t.theme + '</h3>' +
            '<p style="font-size:8px;color:#888;">' + (t.format === 'matching' ? 'Соответствие' : t.format === 'true_false' ? 'True/False/Not stated' : 'Множественный выбор') + '</p>' +
            '<button style="margin-top:10px;">Начать →</button></div>';
    });
    main.innerHTML = html;
}

function startEgeTask(id) {
    const task = EGE_TASKS.find(t => t.id === id);
    if (!task) return;
    window._egeTask = task;
    window._egeAnswers = {};
    renderEgeQuestion();
}

function renderEgeQuestion() {
    const task = window._egeTask;
    const main = document.getElementById('mainContent');
    const fmt = task.format;
    const total = fmt === 'matching' ? task.texts.length : fmt === 'true_false' ? task.statements.length : task.questions.length;

    if (fmt === 'matching') {
        let html = '<div class="card"><h2>🎯 ' + task.theme + '</h2><p style="font-size:8px;">' + task.instruction + '</p>';
        html += '<div style="margin:10px 0;padding:10px;background:var(--accent);border:2px solid var(--border);"><p style="font-size:8px;"><strong>Заголовки:</strong></p>';
        task.headings.forEach((h, i) => { html += '<p style="font-size:8px;">' + (i+1) + '. ' + h + '</p>'; });
        html += '</div>';
        task.texts.forEach((t, i) => {
            const val = window._egeAnswers[i] || '';
            const dot = t.indexOf('.');
            const letter = t.substring(0, dot);
            const textContent = t.substring(dot + 1);
            html += '<div style="border:2px solid var(--border);padding:10px;margin:8px 0;background:var(--card-bg);">' +
                '<p style="font-size:9px;"><strong>' + letter + '.</strong>' + textContent + '</p>' +
                '<p style="font-size:8px;">Заголовок №: <input type="number" min="1" max="7" id="ege_inp_' + i + '" style="width:60px;padding:5px;font-family:inherit;font-size:9px;" value="' + val + '"></p></div>';
        });
        html += '<button onclick="checkEge()">✅ Проверить</button> <button onclick="renderEgePage(document.getElementById(\'mainContent\'))">← Назад</button></div>';
        main.innerHTML = html;
    } else if (fmt === 'true_false') {
        let html = '<div class="card"><h2>🎯 ' + task.theme + '</h2><p style="font-size:8px;">' + task.instruction + '</p>';
        task.statements.forEach((s, i) => {
            const val = window._egeAnswers[i] || '';
            html += '<div style="border:2px solid var(--border);padding:10px;margin:8px 0;background:var(--card-bg);">' +
                '<p style="font-size:9px;">' + (i+1) + '. ' + s + '</p>' +
                '<div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;font-size:9px;">' +
                '<label><input type="radio" name="tf_' + i + '" value="1" ' + (val==1?'checked':'') + '> True</label>' +
                '<label><input type="radio" name="tf_' + i + '" value="2" ' + (val==2?'checked':'') + '> False</label>' +
                '<label><input type="radio" name="tf_' + i + '" value="3" ' + (val==3?'checked':'') + '> Not stated</label></div></div>';
        });
        html += '<button onclick="checkEge()">✅ Проверить</button> <button onclick="renderEgePage(document.getElementById(\'mainContent\'))">← Назад</button></div>';
        main.innerHTML = html;
    } else if (fmt === 'multiple_choice') {
        let html = '<div class="card"><h2>🎯 ' + task.theme + '</h2><p style="font-size:8px;">' + task.instruction + '</p>';
        task.questions.forEach((q, i) => {
            const val = window._egeAnswers[i];
            html += '<div style="border:2px solid var(--border);padding:10px;margin:8px 0;background:var(--card-bg);">' +
                '<p style="font-size:9px;"><strong>' + q.num + '.</strong> ' + q.text + '</p>';
            q.options.forEach((opt, oi) => {
                const checked = val === oi ? 'checked' : '';
                html += '<label style="display:block;font-size:9px;padding:3px 0;"><input type="radio" name="mc_' + i + '" value="' + oi + '" ' + checked + '> ' + opt + '</label>';
            });
            html += '</div>';
        });
        html += '<button onclick="checkEge()">✅ Проверить</button> <button onclick="renderEgePage(document.getElementById(\'mainContent\'))">← Назад</button></div>';
        main.innerHTML = html;
    }
}

function checkEge() {
    const task = window._egeTask;
    const main = document.getElementById('mainContent');
    const fmt = task.format;
    const total = fmt === 'matching' ? task.texts.length : fmt === 'true_false' ? task.statements.length : task.questions.length;
    let correct = 0;
    let results = [];

    for (let i = 0; i < total; i++) {
        let ans = null;
        const inp = document.getElementById('ege_inp_' + i);
        const radios = document.querySelectorAll('input[name="tf_' + i + '"]:checked, input[name="mc_' + i + '"]:checked');
        if (inp) {
            ans = parseInt(inp.value) || null;
        } else if (radios.length) {
            ans = parseInt(radios[0].value);
        }
        const isCorrect = ans === task.correct[i];
        if (isCorrect) correct++;
        results.push(isCorrect);
    }

    let html = '<div class="card"><h2>✅ Результат: ' + correct + '/' + total + '</h2>';
    results.forEach((r, i) => {
        const ca = fmt === 'multiple_choice' && task.questions[i] ? task.questions[i].correct + 1 : task.correct[i];
        html += '<p style="font-size:9px;">' + (r ? '✅' : '❌') + ' Вопрос ' + (i+1) + ': ' + (r ? 'Верно' : 'Ошибка (правильно: ' + ca + ')') + '</p>';
    });
    html += '<button onclick="renderEgePage(document.getElementById(\'mainContent\'))">← К заданиям</button></div>';
    main.innerHTML = html;
}
