# Delta DVP-10MC Series Ethernet Module

> **PLC Communication Library** for C#/.NET applications to interface with Delta DVP-10MC series Ethernet modules.

This library facilitates reading and writing data to the PLC (Digital Inputs, Digital Outputs, Registers) over Ethernet using the Modbus TCP protocol.

---

## Features

- ✅ **Read/Write Digital Inputs** (Bit Access)
- ✅ **Read/Write Digital Outputs** (Bit Access)
- ✅ **Read/Write Registers** (Word Access)
- ✅ **Connection Management** (Connect/Disconnect)
- ✅ **Error Handling** (Robust exception management)

## Prerequisites

- .NET Framework 4.0 or higher
- Delta DVP-10MC Series Module
- Network connectivity between PC and PLC

## Installation

1. **Download** the project or clone the repository.
2. **Build** the solution (Visual Studio).
3. **Add Reference** the compiled DLL (`DeltaDVP10MC.dll`) to your C# project.

## Usage

### Step 1: Add Namespace

```csharp
using DeltaDVP10MC;
```

### Step 2: Initialize Connection

```csharp
try
{
    // Format: "IP Address", Port (Default: 502)
    EthernetTCPClient plc = new EthernetTCPClient("[IP_ADDRESS]", 502);

    plc.Connect();
    Console.WriteLine("Connected to PLC");
    
    // ... perform operations ...
    
    plc.Disconnect();
}
catch (Exception ex)
{
    Console.WriteLine($"Error: {ex.Message}");
}
```

### Step 3: Read/Write Operations

#### Reading Digital Inputs (X)
```csharp
bool[] inputValues = plc.ReadDigitalInputs(0, 10);
// inputValues[0] corresponds to X0
```

#### Writing Digital Outputs (Y)
```csharp
plc.WriteDigitalOutputs(1, new bool[] { true, true, false });
// Sets Y1=True, Y2=True, Y3=False
```

#### Reading Registers (D)
```csharp
ushort d0 = plc.ReadRegister(0);
```

#### Writing Registers (D)
```csharp
plc.WriteRegister(10, 500);
```

## Connection Options

The constructor supports both `string` and `IPAddress` types:

```csharp
// String (Recommended)
var plc1 = new EthernetTCPClient("[IP_ADDRESS]", 502);

// IPAddress Object
var plc2 = new EthernetTCPClient(System.Net.IPAddress.Parse("[IP_ADDRESS]"), 502);
```

## Error Handling

The library throws specific exceptions for:
- Connection issues (`SocketException`, `ArgumentNullException`)
- Communication timeouts (`TimeoutException`)
- Invalid arguments (`ArgumentException`)

Use `try-catch` blocks to handle these gracefully.