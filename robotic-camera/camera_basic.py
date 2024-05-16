from asyncua import Client, Node, ua
import asyncio
import gphoto2 as gp

OPCUA_LOCATION: str = 'oct.tpc://172.32.1.236:4840/server/'
NODE_ID: int = 12  # TODO: Find the correct node id


async def main():
    # set up camera connection
    camera = gp.Camera()
    camera.init(context=None)  # Autodetect and initialise first found camera

    async with Client(url=OPCUA_LOCATION) as client:
        program_start_node = client.get_node(f"ns={NODE_ID};s=C1c_Start")
        trigger_node = client.get_node(f"ns={NODE_ID};s=C1c_Trigger")

    print("Entering Main Polling Loop")
    while True:
        await asyncio.sleep(0.2)

        # Update values from the server
        program_start = await program_start_node.get_value()
        trigger = await trigger_node.get_value()

        # Perform actions on the camera
        if program_start and trigger:
            print("Capturing image")
            camera_file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
            print(f"Image captured: {camera_file_path.name}")
            trigger = False

        # Write values to the server
        await trigger_node.set_value(trigger, ua.VariantType.Boolean)


if __name__ == '__main__':
    asyncio.run(main())
