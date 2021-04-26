import core as oa


def main():
    base_errors = [oa.Response(404, desc='Ничего не найдено'),
                   oa.Response(413, desc='Запрос составлен неверно')]

    member_id_header = oa.HeaderParamener('member_id', default=3441,
                                          desc='Уникальный номер участника, характеризующий'
                                               ' конкретного человека в рамках проекта')

    def _QueryParameter(*args, **kwargs):
        return oa.Parameter(oa.Parameter.QUERY, *args, **kwargs),

    my_api = oa.OpenAPI(
        info=oa.Info(),
        servers=[oa.Server()],
        paths=[
            oa.Path('project'),
            oa.Path('project/findByName',
                    desc='Найти все проекты по имени или его части. Можно также найти по id',
                    requests=[
                        oa.Request(
                            oa.Request.GET,
                            parameters=[
                                _QueryParameter('name', default='fair',
                                                desc='Название проекта, часть названия или id'),
                                member_id_header
                            ],
                            responses=[
                                oa.Response(200, body=oa.Schema())
                            ]
                        )
                    ],
                    responses=[
                        *base_errors,
                        oa.Response(200, content=oa.Schema()),
                    ]),
        ]
    )

    print(my_api.json())


if __name__ == '__main__':
    main()
