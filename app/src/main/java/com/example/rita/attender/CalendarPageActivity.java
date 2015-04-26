package com.example.rita.attender;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import java.util.ArrayList;
import java.util.Arrays;
import android.content.Intent;
import android.app.Activity;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.view.View;

public class CalendarPageActivity extends ActionBarActivity {
    private ListView list;
    private ArrayAdapter<String> adapter;
    private ArrayList<String> arrayList;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_calendar_page);
        list = (ListView) findViewById(R.id.eventslistView);
        arrayList = new ArrayList<String>();
        adapter = new ArrayAdapter<String>(getApplicationContext(), android.R.layout.simple_spinner_item, arrayList);
        list.setAdapter(adapter);
        adapter.add("event1");
        adapter.add("event2");
        adapter.add("event3");
        adapter.add("event4");
        adapter.add("event5");
        adapter.add("event6");
        adapter.add("event7");
        adapter.add("event1");
        adapter.add("event1");
        adapter.add("event1");
        adapter.add("event1");
    }
    public void eventsPressed(View v)
    {
        Intent intent=new Intent(this,searchEventActivity.class);
        startActivity(intent);
    }
    public void chatPressed(View v)
    {
        Intent intent=new Intent(this,ChatPageActivity.class);
        startActivity(intent);
    }
    public void listPressed(View v)
    {
        Intent intent=new Intent(this,Event_Page_Activity.class);
        startActivity(intent);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_calendar_page, menu);
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
