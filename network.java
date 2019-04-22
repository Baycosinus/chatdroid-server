package com.baycosinus.chatdroid;

import android.content.Context;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;
import java.util.Scanner;

public class Network extends AsyncTask<String, Void, Void>
{
    private static String HOST;
    private static int PORT;
    private Exception exception;
    public static boolean status = false;
    private static Context context;
    public static String response;
    Network(Context context, String HOST, int PORT)
    {
        this.context = context;
        this.HOST = HOST;
        this.PORT = PORT;
    }
    public static String getIP()
    {
        WifiManager wifiMan = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
        WifiInfo wifiInf = wifiMan.getConnectionInfo();
        int ipAdress = wifiInf.getIpAddress();
        String ip = String.format("%d.%d.%d.%d", (ipAdress % 0Xff), (ipAdress >> 8 & 0xff),(ipAdress >> 16 & 0xff), (ipAdress >> 16 & 0xff));
        return ip;
    }

    @Override
    protected Void doInBackground(String... params) {
        try {
            Socket writeSocket = new Socket(HOST,PORT);
            PrintWriter writer = new PrintWriter(new OutputStreamWriter(writeSocket.getOutputStream()));
            writer.print(params[0]);
            writer.flush();
            writeSocket.close();


            //Socket socket = new Socket(HOST, PORT);
            ServerSocket serverSocket = new ServerSocket(PORT);
            Socket socket = serverSocket.accept();
            InputStream input = socket.getInputStream();

            BufferedReader reader = new BufferedReader(new InputStreamReader(input));
            String response = reader.readLine();
            Log.e("Server response", response);
            reader.close();
            socket.close();
            serverSocket.close();

            status = true;
        } catch (Exception e) {
            this.exception = e;
            Log.e("Exception",e.toString());
            status = false;
        }
        return null;
    }

    @Override
    protected void onPostExecute(Void result) {
        super.onPostExecute(result);
        Log.e("Log","Async completed.");
    }
}

