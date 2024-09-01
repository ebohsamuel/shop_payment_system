from shop_app.crud import crud_purchase, crud_product
from fastapi import Depends
from shop_app.user_authentication import get_db
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import asyncio

router = APIRouter()
ws_purchase_manager = crud_purchase.WebSocketManager()
ws_sales_manager = crud_product.WebSocketManager()


@router.websocket("/ws/purchases")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    ws_purchase_manager.add_connection(websocket)
    try:
        while True:
            # Broadcast data periodically
            await ws_purchase_manager.broadcast(db)
            await asyncio.sleep(5)  # Adjust the sleep time as needed
    except WebSocketDisconnect:
        ws_purchase_manager.remove_connection(websocket)
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if websocket in ws_purchase_manager.active_connections:
            ws_purchase_manager.remove_connection(websocket)
        await websocket.close()


@router.websocket("/ws/sales")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    ws_sales_manager.add_connection(websocket)
    try:
        while True:
            # Broadcast data periodically
            await ws_sales_manager.broadcast(db)
            await asyncio.sleep(5)  # Adjust the sleep time as needed
    except WebSocketDisconnect:
        ws_sales_manager.remove_connection(websocket)
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if websocket in ws_sales_manager.active_connections:
            ws_sales_manager.remove_connection(websocket)
        await websocket.close()
