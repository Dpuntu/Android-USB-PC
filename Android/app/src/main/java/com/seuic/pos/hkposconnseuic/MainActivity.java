package com.seuic.pos.hkposconnseuic;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

import com.seuic.pos.posconn.OnDownLoadTask;
import com.seuic.pos.posconn.PosConnect;

public class MainActivity extends AppCompatActivity {
    private TextView tt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tt = (TextView) findViewById(R.id.tttt);
        PosConnect.getInstance(MainActivity.this, new OnDownLoadTask() {
            @Override
            public void onProgress(String msg) {
                tt.append(msg + "\r\n");
            }

            @Override
            public void onFail(String msg, int type) {
                tt.append(msg + "\r\n");
            }

            @Override
            public void onSuccess() {
                tt.append("onSuccess\r\n");
            }
        }).connect();

    }
}
