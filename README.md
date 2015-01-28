# CustomUploadWidget
Este  widget customizado para el upload permite previsualizar las imagenes antes de subirlas.

USO :
    
    
    
    model 
    from plugin_widget_upload import CustomUploadWidget
    db.define_table('table_test', Field('imge', 'upload',widget=CustomUploadWidget.widget))

    controller
    upload = URL(c='default',r=request,f='download', args=request.args[:1])
    sqlformargs = dict(upload=upload)
    form = SQLFORM(
                    db.table_test,
                    **sqlformargs
                    )


Despues ire depurando el javascritp que agregue en el widget solo es una prueba temporal.
