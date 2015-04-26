package com.example.rita.attender;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Spinner;
import android.widget.SpinnerAdapter;
import android.widget.ArrayAdapter;
import java.util.ArrayList;
import java.util.Arrays;
import android.content.Intent;
import android.app.Activity;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.view.View;



public class searchEventActivity extends ActionBarActivity {
    private ListView list;
    private ArrayAdapter<String> adapter;
    private ArrayList<String> arrayList;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_event);
        Spinner typeSpinner = (Spinner) findViewById(R.id.type_spinner);
        Spinner dateSpinner = (Spinner) findViewById(R.id.date_spinner);
        Spinner citySpinner = (Spinner) findViewById(R.id.city_spinner);
        list = (ListView) findViewById(R.id.events_listView);
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
        adapter.add("event8");
        adapter.add("event9");
        adapter.add("event10");


        ArrayAdapter<CharSequence> type_adapter = ArrayAdapter.createFromResource(this,
                R.array.type_array, android.R.layout.simple_spinner_item);
        ArrayAdapter<CharSequence> date_adapter = ArrayAdapter.createFromResource(this,
                R.array.dates_array, android.R.layout.simple_spinner_item);
        ArrayAdapter<CharSequence> city_adapter = ArrayAdapter.createFromResource(this,
                R.array.cities_array, android.R.layout.simple_spinner_item);

       type_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
       date_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
       city_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);


        dateSpinner.setAdapter(date_adapter);
        typeSpinner.setAdapter(type_adapter);
        citySpinner.setAdapter(city_adapter);

    }

    public void itemPressed(View v)
    {
        Intent intent=new Intent(this,Event_Page_Activity.class);
        startActivity(intent);
    }
    public void explorePressed(View v)
    {
        Intent intent=new Intent(this,CalendarPageActivity.class);
        startActivity(intent);
    }
    public void chatPressed(View v)
    {
        Intent intent=new Intent(this,ChatPageActivity.class);
        startActivity(intent);
    }
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_search_event, menu);
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
