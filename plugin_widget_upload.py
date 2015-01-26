from gluon import *
from gluon.storage import Storage
from gluon.sqlhtml import *
from gluon.html import BUTTON
_class = 'upload'
DEFAULT_WIDTH = '150px'
ID_DELETE_SUFFIX = '__delete'
GENERIC_DESCRIPTION = 'file ## download'
DELETE_FILE = 'delete'

class CustomUploadWidget(FormWidget):

    @staticmethod
    def widget(field, value,download_url=None,**attributes):
        default = dict(_type='file', )
        attributes = FormWidget._attributes(field, default, **attributes)
        attributes['_class'] = _class
        real_id = attributes['_id']
        fake_id = '%s_fake'%real_id
        button = INPUT(_value='choose file',_type='button',_id=fake_id)
        inp = DIV('',button,DIV(INPUT(**attributes),_style="height:0px;overflow:hidden"))
        img_id = "%s_upload_img"%real_id
        inp['_onchange'] = "loadFile(event,this,'%s')"%img_id

        url = ''

        if download_url and value:
            if callable(download_url):
                url = download_url(value)
            else:
                url = download_url + '/' + value
            (br, image) = ('', '')
            if UploadWidget.is_image(value):
                br = BR()
                image = IMG(_src=url, _width=DEFAULT_WIDTH, _id=img_id)

            requires = attributes["requires"]
            if requires == [] or isinstance(requires, IS_EMPTY_OR):
                inp = DIV(inp,
                          SPAN('[',
                               A(current.T(
                                UploadWidget.GENERIC_DESCRIPTION), _href=url),
                               '|',
                               INPUT(_type='checkbox',
                                     _name=field.name + ID_DELETE_SUFFIX,
                                     _id=field.name + ID_DELETE_SUFFIX),
                               LABEL(current.T(DELETE_FILE),
                                     _for=field.name + ID_DELETE_SUFFIX,
                                     _style='display:inline'),
                               ']', _style='white-space:nowrap'),
                          br, image)
            else:
                inp = DIV(inp,
                          SPAN('[',
                               A(current.T(GENERIC_DESCRIPTION), _href=url),
                               ']', _style='white-space:nowrap'),
                          br, image)
        else:
            image = IMG(_width=DEFAULT_WIDTH, _id=img_id,_alt='')
            inp = DIV(inp,BR(), image)

        javascript = XML("""<script type="text/javascript">
                           jQuery("#%s").click(function () {
                                jQuery("#%s").trigger('click');
                            });
                            
                            var loadFile = function(event,element,img_id) {
                             var reader = new FileReader();
                             reader.onload = function(){
                                 var imageType = /image.*/;
                                 if (!reader.result.match(imageType)) {
                                     return;
                                 }
                                 var output = document.getElementById(img_id);
                                 output.src = reader.result;
                             };
                             reader.readAsDataURL(event.target.files[0]);
                            };
                        </script>"""%(fake_id,real_id))
        return  CAT(inp, javascript)
