using Microsoft.AspNetCore.Mvc;
using System.Collections.Concurrent;

[ApiController]
[Route("[controller]")]
public class SignalingController : ControllerBase
{
    private static readonly ConcurrentDictionary<string, SignalMessage> Messages = new();

    // Endpoint to send offer/answer/candidate
    [HttpPost("send")]
    public IActionResult SendMessage([FromBody] SignalMessage message, [FromQuery] string clientId)
    {
        Messages[clientId] = message;
        return Ok();
    }

    // Endpoint to receive offer/answer/candidate
    [HttpGet("receive")]
    public IActionResult ReceiveMessage([FromQuery] string clientId)
    {
        if (Messages.TryRemove(clientId, out var message))
        {
            return Ok(message);
        }
        return NotFound();
    }
}
