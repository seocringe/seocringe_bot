Использование GitHub Codespaces в Visual Studio Code - Документация по GitHub
created: 2023-08-22T02:14:06 (UTC +03:00)
tags: [Codespaces, Visual Studio Code, Developer]
source: https://docs.github.com/ru/codespaces/developing-in-codespaces/using-github-codespaces-in-visual-studio-code
author:
Использование GitHub Codespaces в Visual Studio Code - Документация по GitHub

    Excerpt

    Можно заниматься разработкой в codespace непосредственно в Visual Studio Code путем подключения расширения GitHub Codespaces к учетной записи в GitHub.

Можно заниматься разработкой в codespace непосредственно в Visual Studio Code путем подключения расширения GitHub Codespaces к учетной записи в GitHub.
Сведения о GitHub Codespaces в Visual Studio Code

Локальная установка Visual Studio Code позволяет создавать кодовыми пространства, управлять ими, работать в таких пространствах и удалять их. Чтобы использовать GitHub Codespaces в VS Code, необходимо установить расширение Codespaces. Дополнительные сведения о настройке GitHub Codespaces в VS Code см. в разделе Предварительные требования.

По умолчанию при создании нового кодовое пространства в GitHub.com оно открывается в браузере. Если вы хотите, чтобы новые кодовые пространства автоматически открывались в VS Code, выберите VS Code как редактор по умолчанию. Дополнительные сведения см. в разделе Настройка редактора по умолчанию для GitHub Codespaces.

Если вы предпочитаете работать в браузере, но хотите продолжать использовать существующие расширения, темы и ярлыки VS Code, вы можете включить синхронизацию параметров. Дополнительные сведения см. в разделе Персонализация GitHub Codespaces для вашей учетной записи.
Предварительные требования

Чтобы заниматься разработкой непосредственно в кодовом пространстве VS Code, установите расширение GitHub Codespaces и выполните вход под своими учетными данными для GitHub. Для расширения GitHub Codespaces требуется VS Code 1.51 за октябрь 2020 года или более поздней версии.

Используйте Visual Studio Code Marketplace для установки расширения GitHub Codespaces. Дополнительные сведения см. в разделе Магазин расширений в документации по VS Code.

    В VS Code на панели действий щелкните значок Удаленного обозревателя.

    Снимок экрана: панель действий. Значок боковой панели Удаленный обозреватель (прямоугольник, наложенный кругом) выделен оранжевым контуром.

    Примечание. Если удаленный обозреватель не отображается на панели действий:
        Откройте палитру команд. Например, нажмите клавиши SHIFT+COMMAND+P (Mac) или CTRL+SHIFT+P (Windows/Linux).
        Введите details.
        Щелкните Codespaces: сведения.

    Выберите GitHub Codespaces в раскрывающемся списке в верхней части боковой панели Удаленный Обозреватель, если она еще не выбрана.

    Щелкните Войти в GitHub.

    Снимок экрана: боковая панель Удаленный Обозреватель для GitHub Codespaces с кнопкой Войти в GitHub.

    Если вы еще не вошли в GitHub, вам будет предложено сделать это. Выполните вход.

    Когда вам будет предложено указать, что вы хотите авторизовать, нажмите кнопку Авторизовать для GitHub.

    Если отображается страница авторизации, щелкните Авторизовать Visual-Studio-Code.

Создание кодового пространства в VS Code

После подключения учетной записи в GitHub.com к расширению GitHub Codespaces можно создать новое пространство кода. Дополнительные сведения о расширении GitHub Codespaces см. в VS Code Marketplace.

    В VS Code на панели действий щелкните значок Удаленного обозревателя.

    Снимок экрана: панель действий. Значок боковой панели Удаленный обозреватель (прямоугольник, наложенный кругом) выделен оранжевым контуром.

    Примечание. Если удаленный обозреватель не отображается на панели действий:
        Откройте палитру команд. Например, нажмите клавиши SHIFT+COMMAND+P (Mac) или CTRL+SHIFT+P (Windows/Linux).
        Введите details.
        Щелкните Codespaces: сведения.

    Наведите указатель мыши на боковую панель Удаленный Обозреватель и щелкните .

    Снимок экрана: боковая панель Удаленный Обозреватель для GitHub Codespaces. Рядом с кнопкой Плюс отображается подсказка Создать новый Codespace.

    В текстовом поле введите имя репозитория, в который вы хотите разработать, а затем выберите его.

    Снимок экрана: octo-org/he, введенный в текстовое поле, и список из четырех репозиториев, которые начинаются с этой строки.

    В правой части последующих подсказок появится сообщение о том, кто будет платить за codespace.

    Снимок экрана: запрос на ветвь с сообщением Использование оплачивается hubwriter.

    Щелкните ветвь, в которой нужно выполнить разработку.

    Если появится запрос на выбор файла конфигурации контейнера разработки, выберите файл из списка.

    Щелкните тип компьютера, в котором нужно выполнить разработку.

Открытие кодового пространства в VS Code

    В VS Code на панели действий щелкните значок Удаленного обозревателя.

    Снимок экрана: панель действий. Значок боковой панели Удаленный обозреватель (прямоугольник, наложенный кругом) выделен оранжевым контуром.

    Примечание. Если удаленный обозреватель не отображается на панели действий:
        Откройте палитру команд. Например, нажмите клавиши SHIFT+COMMAND+P (Mac) или CTRL+SHIFT+P (Windows/Linux).
        Введите details.
        Щелкните Codespaces: сведения.

    В разделе GitHub Codespaces наведите указатель мыши на пространство кода, в которое требуется разработать.

    Щелкните значок подключения (символ вилки).

    Снимок экрана: боковая панель Удаленная Обозреватель. Значок подключения для codespace (символ plug) выделен темно-оранжевым контуром.

Изменение типа компьютера в VS Code

Как правило, вы можете запустить codespace на нескольких типах удаленных компьютеров. Эти типы машин предлагают выбор спецификаций оборудования от 2 до 32 ядер, хотя полный спектр типов машин может быть не всегда доступен. Каждый тип компьютера имеет свой уровень ресурсов и разные уровни выставления счетов. Дополнительные сведения см. в разделе Сведения о выставлении счетов для GitHub Codespaces.

По умолчанию тип компьютера с наименьшими допустимыми ресурсами используется при создании codespace. Тип компьютера для кодового пространства можно изменить в любой момент.

    В VS Code откройте палитру команд с помощью клавиши Command+Shift+P (Mac) или CTRL+SHIFT+P (Windows/Linux).

    Найдите и выберите Кодовые пространства: изменение типа компьютера.

    Снимок экрана: изменить компьютер, введенный в качестве строки поиска, и Codespaces: изменение типа компьютера в раскрывающемся списке.

    Если вы не выполняете эти инструкции в codespace, щелкните codespace, которое требуется изменить.

    Снимок экрана: раскрывающийся список из четырех кодовых пространств.

    Если вы выполняете эти инструкции в codespace, изменение будет применено к пространству кода, с которым вы работаете.

    Выберите тип компьютера, который вы хотите использовать.

    Если вы переходите на тип компьютера с другой емкостью хранилища, появится запрос с запросом на продолжение. Прочтите запрос и нажмите кнопку Да , чтобы принять.

Если вы перешли на виртуальную машину с другой емкостью хранилища (например, с 64 ГБ до 32 ГБ), ваше пространство кода будет недоступно в течение короткого времени, пока изменяется тип компьютера. Если codespace активно, оно будет автоматически остановлено. После завершения изменения вы сможете перезапустить codespace, запущенное на новом типе компьютера.

Если вы перешли на виртуальную машину с той же емкостью хранилища, это изменение будет применено при следующем перезапуске codespace. Активное пространство кода не будет остановлено автоматически. Дополнительные сведения о перезапуске codespace см. в разделе Остановка и запуск пространства кода.
Удаление кодового пространства в VS Code

Можно удалить среды codespace из VS Code, если в настоящее время не работаете в среде codespace.

    В VS Code на панели действий щелкните значок Удаленного обозревателя.

    Снимок экрана: панель действий. Значок боковой панели Удаленный обозреватель (прямоугольник, наложенный кругом) выделен оранжевым контуром.

    Примечание. Если удаленный обозреватель не отображается на панели действий:
        Откройте палитру команд. Например, нажмите клавиши SHIFT+COMMAND+P (Mac) или CTRL+SHIFT+P (Windows/Linux).
        Введите details.
        Щелкните Codespaces: сведения.

    В разделе GitHub Codespaces щелкните правой кнопкой мыши пространство codespace, которое требуется удалить.

    Нажмите кнопку Удалить codespace.

Переход на VS Code участников программы предварительной оценки в веб-клиенте

Если вы используете веб-клиент VS Code, вы можете перейти на версию приложения для участников программы предварительной оценки. Дополнительные сведения об этой версии VS Code см. в статье Введение в сборку участников программы предварительной оценки в блоге VS Code.

После переключения версий в codespace веб-клиент будет продолжать использовать версию участников программы предварительной оценки, если остановить и перезапустить codespace. Новые codespace, создаваемые и открытые в веб-клиенте VS Code, также будут использовать версию участников программы предварительной оценки.

    В левом нижнем углу окна браузера, в котором отображается codespace, щелкните .

    В меню выберите Переключиться на версию участников программы предварительной оценки.

    Снимок экрана: веб-клиент VS Code. Значок шестеренки выделен оранжевым контуром. В меню отображается пункт Переключиться на версию участников программы предварительной оценки.

    Щелкните Перезагрузить.

Чтобы вернуться к стабильной версии VS Code, повторите процесс, но выберите Переключиться на стабильную версию. После обратного переключения codespace продолжит использовать стабильную версию, если остановить и перезапустить codespace. Новые codespace, создаваемые и открытые в веб-клиенте VS Code, также будут использовать стабильную версию.
Использование классического приложения участников программы предварительной оценки для Codespaces

Чтобы использовать GitHub Codespaces в версии программы предварительной оценки классического приложения VS Code, запустите или создайте codespace в приложении программы предварительной оценки VS Code. Дополнительные сведения см. в разделах Создание codespace в VS Codeи Открытие пространства кода в VS Code ранее в этой статье.
Дополнительные материалы

    Использование палитры команд Visual Studio Code в GitHub Codespaces
    Использование GitHub Copilot в GitHub Codespaces
