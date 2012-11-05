
class Message extends Spine.Model
    @configure "Message", "text", "purpose", "tags", "created"

    @extend TransportModel

this.Message = Message