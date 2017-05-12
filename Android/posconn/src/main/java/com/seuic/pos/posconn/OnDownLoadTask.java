package com.seuic.pos.posconn;

/**
 * Created by Dpuntu on 2017/5/12.
 */

public interface OnDownLoadTask {
    void onProgress(String msg);

    void onFail(String msg, int type);

    void onSuccess();
}
