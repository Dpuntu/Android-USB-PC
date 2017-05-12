package com.seuic.pos.posconn;

import android.content.Context;
import android.os.Handler;
import android.os.Message;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * Created by Dpuntu on 2017/5/12.
 */

public class PosConnect {
    public static final String TAG = "PosConnect";
    public static Boolean mainThreadFlag = true;
    public static Boolean ioThreadFlag = true;
    private ServerSocket serverSocket = null;
    private final int SERVER_PORT = 10086;

    private OnDownLoadTask mOnDownLoadTask;
    private static PosConnect mPosConnect;
    private Context context;

    private PosConnect(Context context, OnDownLoadTask mOnDownLoadTask) {
        this.context = context;
        this.mOnDownLoadTask = mOnDownLoadTask;
    }

    public static PosConnect getInstance(Context context, OnDownLoadTask mOnDownLoadTask) {
        if (mPosConnect == null)
            mPosConnect = new PosConnect(context, mOnDownLoadTask);
        return mPosConnect;
    }

    public void connect() {
        disConnect();
        try {
            mOnDownLoadTask.onProgress("正在打开服务");
            Runtime.getRuntime().exec("adb forward tcp:12580 tcp:10086");
            mOnDownLoadTask.onProgress("打开服务成功");
        } catch (Exception e) {
            mOnDownLoadTask.onProgress("打开服务失败，Exception : " + e);
            e.printStackTrace();
        }
        mainThreadFlag = true;
        new Thread() {
            public void run() {
                doListen();
            }
        }.start();
    }

    public void disConnect() {
        mOnDownLoadTask.onProgress("正在关闭服务");
        mainThreadFlag = false;
        ioThreadFlag = false;
        try {
            if (serverSocket != null) serverSocket.close();
            mOnDownLoadTask.onProgress("关闭服务成功");
        } catch (IOException e) {
            mOnDownLoadTask.onProgress("关闭服务失败，IOException : " + e);
            e.printStackTrace();
        }
    }

    private void doListen() {
        serverSocket = null;
        try {
            serverSocket = new ServerSocket(SERVER_PORT);
            while (mainThreadFlag) {
                Socket socket = serverSocket.accept();
                new Thread(new RwSocket(context, socket, mHandler)).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private Handler mHandler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            switch (msg.what) {
                case ConnectProgress.PRO_EXIT:
                    mOnDownLoadTask.onSuccess();
                    break;
                case ConnectProgress.PRO_RECEIVE:
                    mOnDownLoadTask.onProgress("接收到的数据 ：" + msg.obj);
                    break;
            }
        }
    };
}
