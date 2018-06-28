html.Div(
                                [
                                    html.Div(
                                        [
                                            #html.Img(id='LLR, (E)TR, LLR/(E)TR-pie-2017-MOS-img'),

                                            dcc.Graph(id='pie_graph_def_sale_lease_1q_2018', # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 ВСЕ СДЕЛКИ
                                                      figure=my_graphics.update_pie_graph_def_sale_lease_1q_2018_ru(),
                                                      style={'display': 'inline'}
                                                      ),
                                            html.Div(children='Объем сделок аренды и продаж по России в 1кв. 2018',
                                                     style={'padding-left': '70px',
                                                            'display': 'inline',
                                                            'font-weight': 'bold'
                                                            }
                                                     )
                                        ],
                                        className='four columns',
                                    ),
                                    html.Div(
                                        [
                                            #html.Img(id='LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS-img'),

                                            dcc.Graph(id='pie_graph_def_lease_1q_2018',
                                                      # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 АРЕНДА
                                                      figure=my_graphics.update_pie_graph_def_lease_1q_2018_ru(),
                                                      style={'display': 'inline'}
                                                      ),

                                            html.Div(children='Объем сделок аренды по России в 1кв. 2018',
                                                     style={'padding-left': '70px',
                                                            'display': 'inline',
                                                            'font-weight': 'bold'
                                                            }
                                                     )

                                        ],
                                        className='four columns',
                                    ),
                                    html.Div(
                                        [
                                            #html.Img(id='LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS-img'),

                                            dcc.Graph(id='pie_graph_def_sale_1q_2018',
                                                      # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 ПРОДАЖА
                                                      figure=my_graphics.update_pie_graph_def_sale_1q_2018_ru(),
                                                      style={
                                                             'display': 'inline',
                                                             }
                                                      ),
                                            html.Div(children='Объем сделок аренды по России в 1кв. 2018',
                                                     style={'padding-left': '60px',
                                                            'display': 'inline',
                                                            'font-weight': 'bold'
                                                            }
                                                     )
                                        ],
                                        className='four columns',

                                    ),





                                    html.Div(
                                        [

                                            dcc.Graph(id='pie_graph_def_sale_lease_2017_ru',
                                                      # pie по ДОЛЯ РЫНКА ПО РОССИИ В 2017 ВСЕ СДЕЛКИ
                                                      figure=my_graphics.update_pie_graph_def_sale_lease_2017_ru()),
                                            dcc.Graph(id='pie_graph_def_lease_2017_ru',
                                                      # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 АРЕНДА
                                                      figure=my_graphics.update_pie_graph_def_lease_2017_ru()),
                                            dcc.Graph(id='pie_graph_def_sale_2017_ru',
                                                      # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 ПРОДАЖА
                                                      figure=my_graphics.update_pie_graph_def_sale_2017_ru()),
                                            dcc.Graph(id='pie_graph_def_sale_lease_2q_2018',
                                                      figure=my_graphics.update_pie_graph_def_sale_lease_2q_2018_ru()),
                                            dcc.Graph(id='pie_graph_def_lease_1q_2018',
                                                      figure=my_graphics.update_pie_graph_def_lease_2q_2018_ru()),
                                            dcc.Graph(id='pie_graph_def_sale_1q_2018',
                                                      figure=my_graphics.update_pie_graph_def_sale_2q_2018_ru())

                                        ],
                                        className='four columns',
                                        # style={'width': '30.3%',
                                        #        'display': 'row',
                                        #        'float': 'left'}
                                    ),
                                ],
                                className='twelve columns'
                            ),