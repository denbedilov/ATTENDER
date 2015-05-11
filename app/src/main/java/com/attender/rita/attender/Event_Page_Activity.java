package com.attender.rita.attender;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

import com.attender.R;


public class Event_Page_Activity extends Activity {
    Event currEvent;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        TextView tv;
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_event__page_);
        Intent myIntent=getIntent();
        currEvent=  (Event)myIntent.getSerializableExtra("CurrentEvent");

        //==========  DATE   ==================
        tv =(TextView)findViewById(R.id.date_lbl);  //TODO - ADD DATE
        tv.setText(currEvent.getDate());

        //==========  NAME   ==================
        tv =(TextView)findViewById(R.id.evName_lbl);
        tv.setText(currEvent.getName());

        //==========  TIME   ==================
        tv =(TextView)findViewById(R.id.time_lbl);
        tv.setText(currEvent.getTime());

        //==========  CITY   ==================
        tv =(TextView)findViewById(R.id.cityName_lbl);
        tv.setText(currEvent.getCity());

        //==========  ADDRESS   ==================
        tv =(TextView)findViewById(R.id.address_lbl);
        tv.setText(currEvent.getAddress());

        //==========  DESCRIPTION   ==================
        tv =(TextView)findViewById(R.id.description_lbl);    ///TO ADD
        tv.setText(currEvent.getDescription());

        //==========  EVENT URL   ==================
        tv =(TextView)findViewById(R.id.url_lbl);
        tv.setText(currEvent.getEventUrl());

        //==========  HOST   ==================
        tv =(TextView)findViewById(R.id.host_lbl);
        tv.setText(currEvent.getHost());

        //==========  PRICE   ==================
        tv =(TextView)findViewById(R.id.price_lbl);  //chang to price
        tv.setText(currEvent.getPrice());

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_event__page_, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
