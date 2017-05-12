package com.seuic.pos.posconn;

import android.content.Context;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;


public class RwSocket implements Runnable {
    private Socket client;
    private Context context;
    private Handler mHandler;

    public RwSocket(Context context, Socket client, Handler mHandler) {
        this.client = client;
        this.context = context;
        this.mHandler = mHandler;
    }

    @Override
    public void run() {
        BufferedOutputStream out;
        BufferedInputStream in;
        try {
            /* PC端发来的数据msg */
            String currCMD = "";
            out = new BufferedOutputStream(client.getOutputStream());
            in = new BufferedInputStream(client.getInputStream());
            PosConnect.ioThreadFlag = true;
            while (PosConnect.ioThreadFlag) {
                try {
                    if (!client.isConnected()) {
                        break;
                    }
                    /* 接收PC发来的数据 */
                    /* 读操作命令 */
                    currCMD = readCMDFromSocket(in);
                    Log.i(PosConnect.TAG, "currCMD = " + currCMD);
                    if (currCMD.equalsIgnoreCase("exit")) {
                        out.write("exit ok".getBytes("utf-8"));
                        out.flush();
                        PosConnect.ioThreadFlag = false;
                        mHandler.sendEmptyMessage(ConnectProgress.PRO_EXIT);
                    } else {
                        Log.i(PosConnect.TAG, Thread.currentThread().getName() + "---->" + "currCMD ==== " + currCMD);
                        Message msg = mHandler.obtainMessage();
                        msg.what = ConnectProgress.PRO_RECEIVE;
                        msg.obj = currCMD;
                        mHandler.sendMessage(msg);
                        out.write("OK".getBytes("utf-8"));
                        out.flush();
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            Log.i(PosConnect.TAG, "服务关闭");
            out.close();
            in.close();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (client != null) {
                    client.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    /* 读取命令 */
    public String readCMDFromSocket(InputStream in) {
        int MAX_BUFFER_BYTES = 2048;
        String msg = "";
        byte[] tempbuffer = new byte[MAX_BUFFER_BYTES];
        try {
            int numReadedBytes = in.read(tempbuffer, 0, tempbuffer.length);
            msg = new String(tempbuffer, 0, numReadedBytes, "utf-8");
            tempbuffer = null;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return msg;
    }
}