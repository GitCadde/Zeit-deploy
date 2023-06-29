window.addEventListener('load', () => {

    // Aufgabeneingabe-Formular
    const form = document.querySelector('#task-form');
    const input = document.querySelector('#task-input');
    const taskList = document.querySelector('#tasks');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const task = capitalise(input.value);

        if (!task) {
            alert("Bitte fügen Sie eine Aufgabe hinzu");
            return;
        }

        const taskEl = document.createElement('div');
        taskEl.classList.add('task');
        taskList.appendChild(taskEl);

        const contentEl = document.createElement('div');
        contentEl.classList.add('content');
        taskEl.appendChild(contentEl);

        const inputEl = document.createElement('input');
        inputEl.classList.add('text');
        inputEl.type = 'text';
        inputEl.value = task;
        inputEl.readOnly = true;
        contentEl.appendChild(inputEl);

        const counterEl = document.createElement('div');
        counterEl.classList.add('counter');
        taskEl.appendChild(counterEl);

        const timeEl = document.createElement('div');
        timeEl.classList.add('time');
        timeEl.innerText = "00:00:00";
        counterEl.appendChild(timeEl);

        const controlsEl = document.createElement('div');
        controlsEl.classList.add('controls');
        counterEl.appendChild(controlsEl);

        const startBtn = document.createElement('button');
        startBtn.classList.add('start');
        startBtn.innerText = "Starten";
        controlsEl.appendChild(startBtn);

        const stopBtn = document.createElement('button');
        stopBtn.classList.add('stop');
        stopBtn.innerText = "Stoppen";
        controlsEl.appendChild(stopBtn);

        const resetBtn = document.createElement('button');
        resetBtn.classList.add('reset');
        resetBtn.innerText = "Zurücksetzen";
        controlsEl.appendChild(resetBtn);

        const actionsEl = document.createElement('div');
        actionsEl.classList.add('actions');
        taskEl.appendChild(actionsEl);

        const editBtn = document.createElement('button');
        editBtn.classList.add('edit');
        editBtn.innerText = "Aufgabe bearbeiten";
        actionsEl.appendChild(editBtn);

        const deleteBtn = document.createElement('button');
        deleteBtn.classList.add('delete');
        deleteBtn.innerText = "Aufgabe löschen";
        actionsEl.appendChild(deleteBtn);

        input.value = "";

        let seconds = 0;
        let interval = null;

        startBtn.addEventListener('click', start);
        stopBtn.addEventListener('click', stop);
        resetBtn.addEventListener('click', reset);

        function capitalise(str) {
            return str[0].toUpperCase() + str.slice(1);
        }

        function timer() {
            seconds++;

            let hrs = Math.floor(seconds / 3600);
            let mins = Math.floor((seconds - (hrs * 3600)) / 60);
            let secs = seconds % 60;

            if (secs < 10) secs = '0' + secs;
            if (mins < 10) mins = '0' + mins;
            if (hrs < 10) hrs = '0' + hrs;

            timeEl.innerText = `${hrs}:${mins}:${secs}`;
        }

        function start() {
            if (interval) {
                return;
            }

            interval = setInterval(timer, 1000);
        }

        function stop() {
            clearInterval(interval);
            interval = null;
        }

        function reset() {
            stop();
            seconds = 0;
            timeEl.innerText = "00:00:00";
        }

        editBtn.addEventListener('click', () => {
            if (editBtn.innerText.toLowerCase() === 'aufgabe bearbeiten') {
                inputEl.removeAttribute('readonly');
                inputEl.focus();
                editBtn.innerText = "Speichern";
            } else {
                inputEl.setAttribute('readonly', 'readonly');
                editBtn.innerText = "Aufgabe bearbeiten";
            }
        });

        deleteBtn.addEventListener('click', () => {
            taskList.removeChild(taskEl);
        });
    });
});
