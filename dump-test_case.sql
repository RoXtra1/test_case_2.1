CREATE DATABASE test_case; -- создание БД, должно выполняться отдельно от следующих команд

CREATE TABLE public."user" ( -- создание таблицы в БД для юзера
    id character varying(120) NOT NULL,
    password_hash text,
    id_type character varying(10),
    PRIMARY KEY (id)
   );

INSERT INTO public."user" (id,password_hash,id_type) VALUES -- вставка тестового значения, получено после регистрации
	 ('user@mail.ru', -- это почта (id). Пароль - "some password" без кавычек, ниже его хэш
	 'scrypt:32768:8:1$TQHeuYLkjNrqSS6r$ed373d7f00bac124cba3d328ab1d82459d4cc3fdb2011f3264182b3095f3974021b1308e1c85f0e61cd1958a64c9b611a77cde9f8f7a35d29cfe9e8ef947a93b',
	 'mail'
	 );