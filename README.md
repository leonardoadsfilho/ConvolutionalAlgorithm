```javascript
disciplinas = "M/M/1 || M/M/m"
Tipo de entrada = JSON
{
    "numero_de_clientes" = number (N),
    "numero_de_filas" = number (m),
    "taxa_de_servico_e_disciplina_da_fila" = [
        {
            "taxa_de_servico_servico_x1" = number (u1),
            "disciplina_x1" = string
        },
        {
            "taxa_de_servico_servico_x..." = number (u...),
            "disciplina_x..." = string
        },
        {
            "taxa_de_servico_servico_xk" = number (uk),
            "disciplina_xk" = string
        },
    ]
}
```