public class SignalMessage
{
    public string Type { get; set; }  // "offer", "answer", "candidate"
    public string Content { get; set; } // SDP or candidate information
}
