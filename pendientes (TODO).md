# Pendientes para terminar migración

### **Conflictos misc.**
- ~~Tabla trans: ¿qué hace rol?~~ Sol: Se actuailiza el campo según el tipo de persona. commit: 
- Terminar la tabla de vhs_dvd (unica):
    - ~~Se termina la conexión y se checa el proc.  de Berna~~: 05913411847dc2b421165cf9272d7eacda17fa34
    - ~~INSERTAR A LA TABLA cd_vhs_dvd, trans_interpretes, cd_interpretes, cd_item_digital????~~ 0eef7622f33a86777bd6a615ae9b2fc9a489a85d
    - ~~Pasar a TIME, duración (vhs_dvd). (regrear a TIME en bd)~~+ 64f289a421bf088b823735c9b322a3e19bb059df
- ~~Hacer los interpretes, y tal vez item_digital? de las tablas restantes~~
    - ~~Interpretes de FotoRodajes~~ 0119b8972f8826afea4e1befb3247bf1ec1bd52f
    - ~~Interpretes de FotoMontajes~~ fd1147f0df16da93344321ce9b5412e4501e4ba4
- ~~cat_values de las tablas restantes (vhs_dvd, fotomontajes)~~ a52bfef613c64f1af6b4dfd33b112cf34c917ada ,  b4cbd119fc3fe44848617eb5710ffe78df10bed1
- ~~Guardar la fecha original del item en mis tablas, "fechaHoraInsercion" de cd_item~~ a5e6fa30ee97672e5e295a82e0cecbaa43a582e4
- Checar cómo manejar los países que no encontraron match o son dificiles de tratar para encontrar su ISO


#### **Revisar el formato que tendrán datos que no encajaron en su nueva asignaicón de tipo.**
Por ejemplo: *mex (ok) -> mx y usa (cómo?)* 
Lugares donde hay estos conflictos:
- ~~IMAGEN_DIGITAL  (tabla cartel), nota 29 junio~~: Sol: Se decide respetar tipo de dato original, string 
- ... tal vez hay mas.