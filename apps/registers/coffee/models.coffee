
class Message extends Spine.Model
    @configure "Message", "text", "purpose", "tags", "created", "register_id"
    @extend TransportModel

this.Message = Message