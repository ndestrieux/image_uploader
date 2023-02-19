from rest_framework.renderers import BaseRenderer


class JPEGRenderer(BaseRenderer):
    media_type = "image/jpeg"
    format = "jpeg"
    charset = None
    render_style = "binary"

    def render(self, data, media_type=None, renderer_context=None):
        return data


class PNGRenderer(BaseRenderer):
    media_type = "image/png"
    format = "png"
    charset = None
    render_style = "binary"

    def render(self, data, media_type=None, renderer_context=None):
        return data
